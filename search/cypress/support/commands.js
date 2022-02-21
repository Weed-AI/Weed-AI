// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
import 'cypress-file-upload';
import '@testing-library/cypress/add-commands';

Cypress.Commands.add('register', (username, email, password) => {
    cy.clickText(/^Sign up$/)
    cy.get('#username')
    .type(username)
    .should('have.value', username)
    cy.get('#email')
    .type(email)
    .should('have.value', email)
    cy.get('#password')
    .type(password)
    .should('have.value', password)
    cy.findAllByRole('button', /^Sign Up$/).should('have.length', 1).click()
})

Cypress.Commands.add('login', (username, password) => {
    cy.clickText(/^Sign In$/)
    cy.get('#username')
    .type(username)
    .should('have.value', username)
    cy.get('#password')
    .type(password)
    .should('have.value', password)
    cy.findAllByRole('button', /^Sign In$/).should('have.length', 1).click()
})

Cypress.Commands.add('clickText', text => {
    cy.findAllByText(text).should('have.length', 1).click()
})

Cypress.Commands.add('safeSetForm', () => {
    cy.wait(1000)
    // hack needed due to textarea risizing upredictably
    cy.clickText(/JSON data/)
    cy.focused().blur()
    cy.clickText(/^Set Form$/)
})

Cypress.Commands.add('setAgAndMeta', () => {
    cy.clickText(/^Upload and Download Form Contents$/)
    cy.get('.dzu-input').attachFile('test_coco/agcontext.json')
    cy.safeSetForm()
    cy.clickText(/^Next$/)

    cy.findByText(/Dataset Name/i) // Ensure we have proceeded to metadata
    cy.clickText(/^Upload and Download Form Contents$/)
    cy.get('.dzu-input').attachFile('test_coco/metadata.json')
    cy.safeSetForm()
    cy.clickText(/^Next$/)
})