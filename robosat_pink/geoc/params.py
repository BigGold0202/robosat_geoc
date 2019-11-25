class Cover:
    def __init__(self,
                 dir=None,
                 bbox=None,
                 geojson=None,
                 cover=None,
                 raster=None,
                 sql=None,
                 pg=None,
                 no_xyz=None,
                 zoom=None,
                 extent=None,
                 splits=None,
                 out=None):
        # Input [one among the following is required]:
        # plain tiles dir path
        self.dir = dir
        # a lat/lon bbox: xmin,ymin,xmax,ymax or a bbox: xmin,xmin,xmax,xmax,EPSG:xxxx
        self.bbox = bbox
        # a geojson file path
        self.geojson = geojson
        # a cover file path
        self.cover = cover
        # a raster file path
        self.raster = raster

        self.sql = sql
        self.pg = pg

        # Tiles:
        self.no_xyz = no_xyz

        # Outputs:
        # "zoom level of tiles [required with --geojson or --bbox]
        self.zoom = zoom
        self.extent = extent
        self.splits = splits
        self.out = out


class Download:
    def __init__(self,
                 url=None,
                 type="XYZ",
                 rate=10,
                 timeout=10,
                 workers=None,
                 cover=None,
                 format=None,
                 out=None,
                 web_ui_base_url=None,
                 web_ui_template=None,
                 no_web_ui=True):
        # Web Server
        # str, URL server endpoint, with: {z}/{x}/{y} or {xmin},{ymin},{xmax},{ymax} [required]
        self.url = url
        # str, default="XYZ", choices=["XYZ", "WMS"], service type [default: XYZ]
        self.type = type
        # int, default=10, download rate limit in max requests/seconds [default: 10]
        self.rate = rate
        # int, default=10, download request timeout (in seconds) [default: 10]
        self.timeout = timeout
        # int, number of workers [default: CPU / 2]
        self.workers = workers

        # Coverage to download
        # str, path to .csv tiles list [required]
        self.cover = cover

        # Output
        # str, default="webp", file format to save images in [default: webp]
        self.format = format
        # str, output directory path [required]
        self.out = out

        # Web UI
        # str, alternate Web UI base URL
        self.web_ui_base_url = web_ui_base_url
        # str, alternate Web UI template path
        self.web_ui_template = web_ui_template
        # store_true, desactivate Web UI output
        self.no_web_ui = no_web_ui


class Rasterize:
    def __init__(self,
                 cover=None,
                 config=None,
                 type=None,
                 pg=None,
                 sql=None,
                 geojson=None,
                 out=None,
                 append=None,
                 ts=512,
                 web_ui_base_url=None,
                 web_ui_template=None,
                 no_web_ui=True):
        # Inputs [either --postgis or --geojson is required]
        # type=str, path to csv tiles cover file [required]
        self.cover = cover
        self.config = config  # type=str, path to config file [required]
        # type=str, required=True, type of feature to rasterize (e.g Building, Road) [required]
        self.type = type
        # type=str, PostgreSQL dsn using psycopg2 syntax (e.g 'dbname=db user=postgres')
        self.pg = pg
        self.sql = sql  # type=str, help=help)
        self.geojson = geojson  # type=str, path to GeoJSON features files

        # Outputs
        self.out = out  # =str, output directory path [required]
        # action="store_true, Append to existing tile if any, useful to multiclass labels
        self.append = append
        # type=int, default=512,  output tile size[default:512]
        self.ts = ts

        # Web UI
        # type=str, alternate Web UI base URL
        self.web_ui_base_url = web_ui_base_url
        # type=str, alternate Web UI template path
        self.web_ui_template = web_ui_template
        self.no_web_ui = no_web_ui  # action="store_true, desactivate Web UI output


class Subset:
    def __init__(self,
                 dir=None,
                 cover=None,
                 copy=None,
                 delete=None,
                 out=None,
                 web_ui_base_url=None,
                 web_ui_template=None,
                 no_web_ui=True):
        # Inputs:
        # DIR, to XYZ tiles input dir path [required]
        self.dir = dir
        # COVER, path to csv cover file to filter dir by [required]
        self.cover = cover

        # Alternate modes, as default is to create relative symlinks.:
        self.copy = copy  # copy tiles from input to output
        self.delete = delete  # delete tiles listed in cover

        # Output:
        self.out = out  # output dir path [required for copy or move]

        # Web UI:
        # WEB_UI_BASE_URL  alternate Web UI base URL
        self.web_ui_base_url = web_ui_base_url
        # WEB_UI_TEMPLATE  alternate Web UI template path
        self.web_ui_template = web_ui_template
        self.no_web_ui = no_web_ui  # desactivate Web UI output


class Train:
    def __init__(self,
                 config=None,
                 dataset=None,
                 loader=None,
                 workers=None,
                 bs=4,
                 lr=None,
                 ts=None,
                 nn=None,
                 loss=None,
                 da=None,
                 dap=1.0,
                 epochs=10,
                 resume=False,
                 checkpoint=None,
                 no_validation=False,
                 no_training=False,
                 saving=1,
                 out=None):
        # train", Trains a model on a dataset", formatter_class=formatter_class)
        self.config = config  # type=str, path to config file[required]

        # Dataset
        self.dataset = dataset  # type=str, training dataset path
        # type=str, dataset loader name[if set override config file value]
        self.loader = loader
        # type=int, number of pre-processing images workers[default: batch size]
        self.workers = workers

        # Hyper Parameters [if set override config file value]
        self.bs = bs  # type=int, batch size
        self.lr = lr  # type=float, learning rate
        self.ts = ts  # type=int, tile size
        self.nn = nn  # type=str, neurals network name
        self.loss = loss  # type=str, model loss
        self.da = da  # type=str, kind of data augmentation

        # type=float, default=1.0,data augmentation probability[default: 1.0]
        self.dap = dap

        # Model Training
        # type=int, default=10,number of epochs to train[default: 10]
        self.epochs = epochs
        # action="store_true,resume model training, if set imply to provide a checkpoint
        self.resume = resume
        # type=str, path to a model checkpoint. To fine tune or resume a training
        self.checkpoint = checkpoint
        # action="store_true, No validation, training only
        self.no_validation = no_validation
        # action="store_true, No training, validation only
        self.no_training = no_training

        # Output
        # type=int, default=1, number of epochs beetwen checkpoint .pth saving[default: 1]
        self.saving = saving
        # type=str, output directory path to save checkpoint .pth files and logs[required]
        self.out = out


class Predict:
    def __init__(self,
                 dataset=None,
                 checkpoint=None,
                 config=None,
                 out=None,
                 workers=None,
                 bs=4,
                 web_ui_base_url=None,
                 web_ui_template=None,
                 no_web_ui=None):
        # Inputs:
        # dataset, predict dataset directory path [required]
        self.dataset = dataset
        # CHECKPOINT, path to the trained model to use [required]
        self.checkpoint = checkpoint
        self.config = config  # CONFIG, path to config file [required]

        # Outputs:
        self.out = out  # output directory path [required]

        # Data Loaders:
        # WORKERS, number of workers to load images [default: GPU x 2]
        self.workers = workers
        self.bs = bs  # BS, batch size value for data loader [default: 4]

        # Web UI:
        # WEB_UI_BASE_URL  alternate Web UI base URL
        self.web_ui_base_url = web_ui_base_url
        # WEB_UI_TEMPLATE  alternate Web UI template path
        self.web_ui_template = web_ui_template
        self.no_web_ui = no_web_ui  # desactivate Web UI output


class Vectorize:
    def __init__(self,
                 masks=None,
                 type=None,
                 config=None,
                 out=None):
        # Inputs:
        # input masks directory path [required]
        self.masks = masks
        # type of features to extract (i.e class title) [required]
        self.type = type
        # path to config file [required]
        self.config = config

        # Outputs:
        # path to output file to store features in [required]
        self.out = out


class Features:# masks --type --dataset out
    def __init__(self,
                 masks=None,
                 type=None,
                 dataset=None,
                 out=None):
        # Inputs:
        # input masks directory path [required]
        self.masks = masks
        # type of features to extract (i.e class title) [required]
        self.type = type
        # path to config file [required]
        self.dataset = dataset

        # Outputs:
        # path to output file to store features in [required]
        self.out = out


class Merge:# features --threshold out
    def __init__(self,
                 features=None,
                 threshold=None,
                 out=None):
        # Inputs:
        # input masks directory path [required]
        self.features = features
        # type of features to extract (i.e class title) [required]
        self.threshold = threshold

        # Outputs:
        # path to output file to store features in [required]
        self.out = out