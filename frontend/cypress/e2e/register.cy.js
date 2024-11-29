describe('User Registration Flow', () => {
  beforeEach(() => {
    cy.visit('/register');
  });

  it('should load the registration page correctly', () => {
    // Check that the page loads and initial step is visible
    cy.contains('Step 1: Account Info').should('be.visible');
    cy.get('input[placeholder="Username"]').should('be.visible');
    cy.get('input[placeholder="Password"]').should('be.visible');
    cy.get('input[placeholder="Confirm Password"]').should('be.visible');
  });

  it('should navigate through registration steps', () => {
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
    cy.url().should('include', '/login');
  });

  it('should prevent submission with invalid inputs', () => {
    // Step 1: Invalid password confirmation
    cy.get('input[placeholder="Username"]').type('testuser');
    cy.get('input[placeholder="Password"]').type('StrongPass123!');
    cy.get('input[placeholder="Confirm Password"]').type('DifferentPassword');
    
    // Move to Step 2 should not be possible
    cy.contains('button', 'Next').should('be.disabled');

    // Correct the password
    cy.get('input[placeholder="Confirm Password"]').clear().type('StrongPass123!');
    cy.contains('button', 'Next').click();

    // Step 2
    cy.get('input[placeholder="First Name"]').type('John');
    cy.get('input[placeholder="Last Name"]').type('Doe');
    cy.get('input[type="date"]').type('1990-01-01');
    cy.contains('button', 'Next').click();

    // Step 3: Invalid email
    cy.get('input[placeholder="Phone Number"]').type('1234567890');
    cy.get('input[placeholder="Email"]').type('invalidemail');
    
    // Submit should not work
    cy.contains('button', 'Submit').click();
    
    // Expect to remain on the registration page
    cy.url().should('include', '/register');
  });

  it('should have a working previous button', () => {
    // Navigate to Step 2
    cy.get('input[placeholder="Username"]').type('testuser');
    cy.get('input[placeholder="Password"]').type('StrongPass123!');
    cy.get('input[placeholder="Confirm Password"]').type('StrongPass123!');
    cy.contains('button', 'Next').click();

    // Go back to Step 1
    cy.contains('button', 'Previous').click();
    cy.contains('Step 1: Account Info').should('be.visible');

    // Verify data is preserved
    cy.get('input[placeholder="Username"]').should('have.value', 'testuser');
    cy.get('input[placeholder="Password"]').should('have.value', 'StrongPass123!');
  });

  it('should handle API errors', () => {
    // Intercept the registration API call and force an error
    cy.intercept('POST', '/users/register', {
      statusCode: 400,
      body: { error: 'Username already exists' }
    }).as('registerFail');

    // Fill out the entire form
    cy.get('input[placeholder="Username"]').type('testuser');
    cy.get('input[placeholder="Password"]').type('StrongPass123!');
    cy.get('input[placeholder="Confirm Password"]').type('StrongPass123!');
    cy.contains('button', 'Next').click();

    cy.get('input[placeholder="First Name"]').type('John');
    cy.get('input[placeholder="Last Name"]').type('Doe');
    cy.get('input[type="date"]').type('1990-01-01');
    cy.contains('button', 'Next').click();

    cy.get('input[placeholder="Phone Number"]').type('1234567890');
    cy.get('input[placeholder="Email"]').type('johndoe@example.com');

    // Submit and wait for error response
    cy.contains('button', 'Submit').click();
    cy.wait('@registerFail');

    // Check for error alert
    cy.on('window:alert', (str) => {
      expect(str).to.equal('Username already exists');
    });

    // Should remain on registration page
    cy.url().should('include', '/register');
  });
});