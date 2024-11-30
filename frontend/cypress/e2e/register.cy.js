describe('User Registration Flow', () => {
  beforeEach(() => {
    // Visit the registration page before each test
    cy.visit('/register');
  });

  it('should load the registration page correctly', () => {
    // Check that the page loads and initial step is visible
    cy.contains('Step 1: Account Info').should('be.visible');
    cy.get('input[placeholder="Username"]').should('be.visible');
    cy.get('input[placeholder="Password"]').should('be.visible');
    cy.get('input[placeholder="Confirm Password"]').should('be.visible');
  });

  it('Should navigate through registration steps and display username taken', () => {
    // Step 1: Account Info
    cy.get('input[placeholder="Username"]').type('testuser');
    cy.get('input[placeholder="Password"]').type('StrongPass123!');
    cy.get('input[placeholder="Confirm Password"]').type('StrongPass123!');
    
    // Move to Step 2
    cy.contains('button', 'Next').click();
    cy.contains('Step 2: Personal Info').should('be.visible');

    // Step 2: Personal Info
    cy.get('input[placeholder="First Name"]').type('John');
    cy.get('input[placeholder="Last Name"]').type('Doe');
    cy.get('input[type="date"]').type('1990-01-01');

    // Move to Step 3
    cy.contains('button', 'Next').click();
    cy.contains('Step 3: Contact Info').should('be.visible');

    // Step 3: Contact Info
    cy.get('input[placeholder="Phone Number"]').type('1234567890');
    cy.get('input[placeholder="Email"]').type('johndoe@example.com');

    // Submit the form
    cy.contains('button', 'Submit').click();

    // Assert navigation to login page or success message
    cy.on('window:alert', (str) => {
      expect(str).to.equal('Username already taken');
    });
  });

  it('Should not allow registration to happend with empty fields', () => {
    
    // Move to Step 2
    cy.contains('button', 'Next').click();
    cy.contains('Step 2: Personal Info').should('be.visible');

    // Move to Step 3
    cy.contains('button', 'Next').click();
    cy.contains('Step 3: Contact Info').should('be.visible');

    // Submit the form
    cy.contains('button', 'Submit').click();

    cy.on('window:alert', (str) => {
      expect(str).to.equal('Please fill out this field');
    });
  });
});