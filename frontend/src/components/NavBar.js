import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Container from '@mui/material/Container';
import MenuItem from '@mui/material/MenuItem';
import logo from '../assets/logo-navbar.png'; 

export function NavBar()  {
  const pages = ['Home', 'Blockchain', 'Conduct a Transaction', 'Transaction Pool'];
  const pageLinks = ['/', '/blockchain', '/conduct-transaction', '/transaction-pool']; 

  return (
    <AppBar position="fixed" sx={{bgcolor: '#212121'}}>
      <Container>
        <Toolbar>
          <img
            src={logo}
            alt="Logo"
            style={{ marginRight: '10px', width: 30, height: 30 }}
          />
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'flex' } }}>
            {pages.map((page, index) => (
              <MenuItem key={page} component="a" href={pageLinks[index]} sx={{fontSize: '1.50rem'}}>
                {page}
              </MenuItem>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default NavBar;