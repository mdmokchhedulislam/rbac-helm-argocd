const express = require('express');
const app = express();
const port = process.env.PORT || 4002;

// Helmet for security
const helmet = require('helmet');
app.use(helmet());

// Body parser middleware
app.use(express.json());

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to Industry Standard Node.js Application',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/v1/healthz', (req, res) => {
  res.status(200).json({ status: 'OK', message: 'Service is healthy' });
});

app.get('/api/v1/users', (req, res) => {
  res.json({
    users: [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
    ]
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});