import sys
import uuid
import torch
import torch.onnx
import torch.autograd

import robosat_pink as rsp
from robosat_pink.core import load_module


def add_parser(subparser, formatter_class):
    parser = subparser.add_parser("export", help="Export a model to ONNX or Torch JIT", formatter_class=formatter_class)

    inp = parser.add_argument_group("Inputs")
    inp.add_argument("--checkpoint", type=str, required=True, help="model checkpoint to load [required]")
    inp.add_argument("--type", type=str, choices=["onnx", "jit", "pth"], default="onnx", help="output type [default: onnx]")

    pth = parser.add_argument_group("To set or override metadata pth parameters:")
    pth.add_argument("--nn", type=str, help="nn name")
    pth.add_argument("--loader", type=str, help="nn loader")
    pth.add_argument("--doc_string", type=str, help="nn documentation abstract")
    pth.add_argument("--shape_in", type=str, help="nn shape in (e.g 3,512,512)")
    pth.add_argument("--shape_out", type=str, help="nn shape_out  (e.g 2,512,512)")

    out = parser.add_argument_group("Output")
    out.add_argument("out", type=str, help="path to save export model to [required]")

    parser.set_defaults(func=main)


def main(args):

    chkpt = torch.load(args.checkpoint, map_location=torch.device("cpu"))
    UUID = chkpt["uuid"] if "uuid" in chkpt else uuid.uuid1()

    try:
        nn_name = chkpt["nn"]
    except:
        assert args.nn, "--nn mandatory as not already in input .pth"
        nn_name = args.nn

    try:
        loader = chkpt["loader"]
    except:
        assert args.loader, "--loader mandatory as not already in input .pth"
        doc_string = args.doc_string

    try:
        doc_string = chkpt["doc_string"]
    except:
        assert args.doc_string, "--doc_string mandatory as not already in input .pth"
        doc_string = args.doc_string

    try:
        shape_in = chkpt["shape_in"]
    except:
        assert args.shape_in, "--shape_in mandatory as not already in input .pth"
        shape_in = tuple(map(int, args.shape_in.split(",")))

    try:
        shape_out = chkpt["shape_out"]
    except:
        assert args.shape_out, "--shape_out mandatory as not already in input .pth"
        shape_out = tuple(map(int, args.shape_out.split(",")))

    model_module = load_module("robosat_pink.models.{}".format(nn_name.lower()))
    nn = getattr(model_module, nn_name)(shape_in, shape_out).to("cpu")

    print("RoboSat.pink - export model to {}".format(args.type), file=sys.stderr)
    print("Model: {}".format(nn_name, file=sys.stderr))
    print("UUID: {}".format(UUID, file=sys.stderr))

    if args.type == "pth":

        states = {
            "uuid": UUID,
            "model_version": None,
            "producer_name": "RoboSat.pink",
            "producer_version": rsp.__version__,
            "model_licence": "MIT",
            "domain": "pink.RoboSat",  # reverse-DNS
            "doc_string": doc_string,
            "shape_in": shape_in,
            "shape_out": shape_out,
            "state_dict": nn.state_dict(),
            "epoch": 0,
            "nn": nn_name,
            "optimizer": None,
            "loader": loader,
        }

        torch.save(states, args.out)

    else:

        try:  # https://github.com/pytorch/pytorch/issues/9176
            nn.module.state_dict(chkpt["state_dict"])
        except AttributeError:
            nn.state_dict(chkpt["state_dict"])

        nn.eval()

        batch = torch.rand(1, *shape_in)

        if args.type == "onnx":
            torch.onnx.export(
                nn,
                torch.autograd.Variable(batch),
                args.out,
                input_names=["input", "shape_in", "shape_out"],
                output_names=["output"],
                dynamic_axes={"input": {0: "num_batch"}, "output": {0: "num_batch"}},
            )

        if args.type == "jit":
            torch.jit.trace(nn, batch).save(args.out)
