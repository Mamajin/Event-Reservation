describe('Apply for Event and Cancel Registration', () => {
    it('should register for an event, verify it in tickets, and cancel registration', () => {
      cy.visit('/login');
      cy.get('input[placeholder="Username"]').type('testuser');
      cy.get('input[placeholder="Password"]').type('StrongPass123!');
      cy.get('button').contains('Login').click();
      cy.url().should('include', '/');
  
      cy.contains('a', 'Explore Events').click();
      cy.intercept('GET', '/api/events/events').as('getEvents');
      cy.wait('@getEvents');
      cy.get('[data-testid="event-card"]').should('have.length.gt', 0);
  
      cy.get('[data-testid="event-name"]').first().invoke('text').as('selectedEventName');
      cy.get('[data-testid="event-name"]').first().click({ force: true });
      cy.url().should('include', '/events/');
      cy.get('[data-testid="event-header"]').should('be.visible');
  
      cy.contains('button', 'Apply').click();
      cy.on('window:alert', (text) => {
        expect(text).to.contains('Event applied successfully!');
      });
  
      cy.contains('a', 'My Tickets').click();
      cy.url().should('include', '/tickets');
      cy.get('@selectedEventName').then((eventName) => {
        cy.get('[data-testid="ticket-item"]').should('contain', eventName.trim());
      });
  
      cy.contains('a', 'Explore Events').click();
      cy.get('[data-testid="event-name"]').first().click({ force: true });
      cy.contains('button', 'Unapply').click();
      cy.contains('Successfully canceled registration').should('be.visible');
  
      cy.contains('a', 'My Tickets').click();
      cy.get('@selectedEventName').then((eventName) => {
        cy.get('[data-testid="ticket-item"]').should('not.contain', eventName.trim());
      });
    });
  });
  