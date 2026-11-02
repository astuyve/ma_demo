# Massachusetts Age Atlas

Interactive map of median age across Massachusetts' 351 cities and towns and 14 counties. Click a place to see its age distribution against the statewide curve.

Data: U.S. Census Bureau, ACS 2020–2024 5-year estimates (B01001, B01002); 2024 cartographic boundary files.

## Rebuild

```sh
mkdir -p raw/acs raw/cousub build
curl -sL -o raw/acs/b01001.dat https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b01001.dat
curl -sL -o raw/acs/b01002.dat https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b01002.dat
curl -sL -o raw/cousub/cousub.zip https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_25_cousub_500k.zip && (cd raw/cousub && unzip -oq cousub.zip)

python3 -I scripts/build_data.py raw/acs build/ages.json
npx -y mapshaper@0.6.102 raw/cousub/cb_2024_25_cousub_500k.shp -filter 'ALAND>0' -simplify 15% keep-shapes \
  -filter-fields GEOID,NAME,NAMELSAD,COUNTYFP,NAMELSADCO -rename-layers towns \
  -o build/towns.json format=topojson quantization=1e5
python3 -I scripts/build_page.py scripts/template.html build index.html
```
