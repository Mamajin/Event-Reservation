describe('Login and View Event', () => {
    it('should login and navigate to event details', () => {
      cy.visit('/login');
  
      cy.get('input[placeholder="Username"]').type('testuser');
      cy.get('input[placeholder="Password"]').type('StrongPass123!');
  
      cy.get('button').contains('Login').click();
  
      // Wait for login to complete and navigate to home/discover
      cy.url().should('include', '/');
  
      // Navigate to Discover page
      cy.contains('a', 'Explore Events').click();
  
      cy.intercept('GET', '/api/events/events').as('getEvents');
      cy.wait('@getEvents');
  
      // Check that at least one event card exists
      cy.get('[data-testid="event-card"]').should('have.length.gt', 0);
  
      cy.get('[data-testid="event-name"]').first().click({ force: true });
  
      // Assert we're on an event detail page
      cy.url().should('include', '/events/');
  
      cy.get('[data-testid="event-header"]').should('be.visible');
      cy.get('[data-testid="event-info"]').should('be.visible');
      cy.get('[data-testid="event-comment"]').should('be.visible');
      cy.get('[data-testid="event-organizer-info"]').should('be.visible');
    });
  });
  