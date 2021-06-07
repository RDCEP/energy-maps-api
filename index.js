const app = require('express')();
const PORT = 8080;

// JSON Data
const railroads = require('./data/railrdl020.json')
const crude_oil = require('./data/CrudeOil_Pipelines_US_Nov2014_clipped.geojson')
const grid_dc = require('./data/grid-dc.json')
const grid_unk_under_100 = require('./data/grid-unk_under_100.json')
const grid_345_735 =  require('./data/grid-345_735.json')
const grid_1_3 = require('./data/grid-100_300.json')

app.listen(
    PORT,
    () => console.log(`app listening on http://localhost:${PORT}`)
);

app.get('/railroads', (req, res) => {
    res.status(200).send(railroads)
});

app.get('grid_dc', (req, res) => {
    res.status(200).send(grid_dc)
})


app.get('grid_unk_under_100', (req, res) => {
    res.status(200).send(grid_unk_under_100)
})


app.get('grid_345_735', (req, res) => {
    res.status(200).send(grid_345_735)
})