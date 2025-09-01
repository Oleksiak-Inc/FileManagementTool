import { render, screen } from '@testing-library/react';
import App from './App.js';
import { addUser } from './api.mjs';

test('api call addUser', async () => {
  const response = await addUser('Ann', 'ann@mail.com');
  console.log("Test response:", response);

  expect(response).toHaveProperty('name', 'Ann');
});

/*
test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
*/
