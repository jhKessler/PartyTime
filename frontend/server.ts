const express = require('express');
const app = express();
const port = 5000;

const Pool = require('pg').Pool;
const pool = new Pool({
  user: 'partytime',
  host: 'localhost',
  port: 5432,
  database: 'partytime'
});

app.use(express.static(__dirname + '/dist/frontend/'));

app.get('/data', (request, response) => {
  pool.query('select * from history', (err, res) => {
    if(err){
      throw err
    }
    if(res.rows.length == 0){
      response.status(500).json({'error': 'no data'});
      return;
    }
    response.status(200).json(res.rows[res.rows.length - 1].data);
  });
});

app.listen(port, () => console.log(`server listening on ${port}`));
