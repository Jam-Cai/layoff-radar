const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 8000;

app.use(cors());

app.get('/score/:company', (req, res) => {
  const { company } = req.params;

  res.json({
    company,
    risk: 0,
    top_factors: [
    ],
    explanation: `Risk for ${company} is based on _____`
  });
});

app.listen(PORT, () => {
  console.log(`API running at http://localhost:${PORT}`);
});