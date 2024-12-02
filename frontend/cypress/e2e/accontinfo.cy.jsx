describe('Navigate to Account Info and Organizer Info', () => {
    beforeEach(() => {
      cy.visit('/login');
      cy.get('input[placeholder="Username"]').type('testuser');
      cy.get('input[placeholder="Password"]').type('StrongPass123!');
      cy.get('button').contains('Login').click();
  
      cy.url().should('not.include', '/login');
    });
  
    it('should navigate to the Account Info page and verify user details', () => {
        cy.get('.avatar')
        .click();
    
        cy.get('.dropdown-content')
        .contains('Account')
        .should('be.visible')
        .click();
    
        cy.url().should('include', '/account-info');
        cy.wait(1000);

        cy.get('h1').should('contain', 'Account Details');
    
        cy.contains('Username').should('be.visible');
        cy.contains('Address').should('be.visible');
        cy.contains('Nationality').should('be.visible');
        cy.contains('Facebook').should('be.visible');
        cy.contains('Instagram').should('be.visible');

        cy.contains('Edit Profile').should('be.visible');
    });

    it('should navigate to Organizer Profile and check for attributes', () => {
        cy.get('.avatar')
          .click();
    
        cy.get('.dropdown-content')
          .contains('Account')
          .should('be.visible')
          .click();
    
        cy.url().should('include', '/account-info');
    
        cy.contains('Go to Organizer Profile').should('be.visible').click();
    
        cy.url().should('include', '/organizer-info');
    
        cy.get('h1').should('contain', 'Organizer Profile');
        cy.contains('Edit Profile').should('be.visible');
      });
  });