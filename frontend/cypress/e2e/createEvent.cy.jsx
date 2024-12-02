describe('Create Event Page and delete it', () => {
    beforeEach(() => {
      cy.visit('/login');
      cy.get('input[placeholder="Username"]').type('testuser2');
      cy.get('input[placeholder="Password"]').type('StrongPass123!');
      cy.get('button').contains('Login').click();
  
      cy.url().should('not.include', '/login');
    });
  
    it('should allow navigating to create event page via Navbar and creating an event', () => {
      // Verify the Create Event button is visible in the Navbar
      cy.get('.navbar-end .btn')
        .contains('Create Event +')
        .should('be.visible')
        .click();
  
      cy.url().should('include', '/create-event');
      cy.get('h2').should('contain', 'Create Your Event');
  
      cy.get('input[name="event_name"]').type('Cypress Test Event');
      cy.get('textarea[name="description"]').type('This is a test event created via Cypress.');
      cy.get('select[name="category"]').select('CONFERENCE');
      cy.get('select[name="dress_code"]').select('CASUAL');
  
      cy.contains('Location').click();
      cy.get('input#address-input').type('123 Test St, Test City');
  
      cy.contains('Date & Time').click();
      cy.get('input[name="start_date_register"]').type('2024-12-01T09:00');
      cy.get('input[name="end_date_register"]').type('2024-12-05T18:00');
      cy.get('input[name="start_date_event"]').type('2024-12-10T10:00');
      cy.get('input[name="end_date_event"]').type('2024-12-10T15:00');
  
      cy.contains('Ticketing').click();
      cy.get('input[name="is_free"]').uncheck();
      cy.get('input[name="ticket_price"]').type('50');
      cy.get('input[name="max_attendee"]').type('100');
  
      cy.contains('Contact & Social').click();
      cy.get('input[name="contact_email"]').type('testevent@test.com');
      cy.get('input[name="contact_phone"]').type('1234567890');
      cy.get('input[name="facebook_url"]').type('https://facebook.com/testevent');
      cy.get('input[name="twitter_url"]').type('https://twitter.com/testevent');
  
      cy.get('button[type="submit"]').contains('Create Event').click();
  
      cy.on('window:alert', (text) => {
        expect(text).to.contains('Event created successfully!');
      });
    });

    it('should navigate to My Events and delete the created event', () => {
        cy.contains('My Events').click();
      
        cy.url().should('include', '/my-events');
        cy.get('h1').should('contain', 'My Events');
      

        cy.contains('Cypress Test Event')
          .should('be.visible')
          .parent()
          .as('eventRow');
      
        cy.get('@eventRow')
          .find('button')
          .contains('Delete')
          .click();
           
        cy.contains('Cypress Test Event').should('not.exist');
      });
      
      

  });
  