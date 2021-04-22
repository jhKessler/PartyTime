const express = require('express');
const cors = require('cors');

const app = express();
const port = 5000;


const host = process.env.database_host ? process.env.database_host : 'localhost'
const Pool = require('pg').Pool;
const pool = new Pool({
  user: 'partytime',
  host: host,
  port: 5432,
  database: 'partytime'
});

console.log(`connecting to db ${host}`);

app.use(cors());

app.use(express.static(__dirname + '/dist/frontend/'));

app.get('/data', (request, response) => {
  pool.query('select * from history', (err, res) => {
    if (err || res.rows.length == 0) {
      response.status(500).json({'error': 'no data'});
      return;
    }
    response.status(200).json(res.rows[res.rows.length - 1].data);
  });
});

app.listen(port, () => console.log(`server listening on ${port}`));
