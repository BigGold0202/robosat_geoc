--从BUIA整理一个乡为单位的中心点extent
ALTER table data_xiang add COLUMN centroid "public"."geometry";
ALTER table data_xiang add COLUMN centroid_buff "public"."geometry";
update data_xiang set centroid = st_centroid(geom) where st_geometrytype(geom)='ST_GeometryCollection'
update data_xiang set centroid_buff = st_buffer(centroid,0.01) where centroid is not NULL 
--多个geometry变单个geometry，导出geojson
select st_asgeojson(st_union(centroid_buff)) from data_xiang