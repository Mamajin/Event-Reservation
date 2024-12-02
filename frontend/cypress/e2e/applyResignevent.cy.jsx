describe('Event Application and Cancellation Workflow', () => {
  it('should check if an event is already applied and apply if not', () => {
    cy.visit('/login');
    cy.get('input[placeholder="Username"]').type('testuser2');
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

    cy.contains('button', /Apply Now|Unapply/).then(($button) => {
      if ($button.text().includes('Apply Now')) {
        $button.click();
        cy.on('window:alert', (text) => {
          expect(text).to.contains('Event applied successfully!');
        });

        cy.contains('a', 'My Tickets').click();
        cy.url().should('include', '/my-tickets');
        cy.get('@selectedEventName').then((eventName) => {
          cy.get('[data-testid="ticket-item"]').should('contain', eventName.trim());
        });
      } else if ($button.text().includes('Unapply')) {
        cy.log('Event is already applied. Test completed.');
      }
    });

    cy.wait(2000);
  });

  it('should select an event from "My Tickets" and unapply', () => {
    cy.visit('/login');
    cy.get('input[placeholder="Username"]').type('testuser2');
    cy.get('input[placeholder="Password"]').type('StrongPass123!');
    cy.get('button').contains('Login').click();
    cy.url().should('include', '/');

    cy.contains('a', 'My Tickets').click();
    cy.url().should('include', '/my-tickets');

    cy.get('[data-testid="ticket-item"]').first().invoke('text').as('ticketEventName');
    cy.get('[data-testid="ticket-item"]').first()
    .find('img')
    .should('be.visible')
    .click({ force: true });

    cy.url().should('include', '/events/');
    cy.get('[data-testid="event-header"]').should('be.visible');

    cy.intercept('POST', '/api/events/unapply').as('unapplyEvent');
    cy.contains('button', 'Unapply').click();
    cy.wait('@unapplyEvent').then((interception) => {
      console.log(interception.response);
      expect(interception.response.statusCode).to.eq(200);
    });
    cy.on('window:alert', (text) => {
      expect(text).to.be.oneOf([
        'You have successfully unapplied from the event!',
        'Failed to unapply from the event.'
      ]);
    });

    cy.contains('a', 'My Tickets').click();
    cy.get('@ticketEventName').then((eventName) => {
      cy.get('[data-testid="ticket-item"]').should('not.contain', eventName.trim());
    });
  });
});
