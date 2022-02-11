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

let selectedValueGlobal = ''

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

// CVAT Commands
Cypress.Commands.add('cvat_login', (username, password) => {
    cy.get('[placeholder="Username"]').type(username);
    cy.get('[placeholder="Password"]').type(password);
    cy.get('[type="submit"]').click();
    cy.url().should('match', /\/tasks$/);
    cy.document().then((doc) => {
        const loadSettingFailNotice = Array.from(doc.querySelectorAll('.cvat-notification-notice-load-settings-fail'));
        if (loadSettingFailNotice.length > 0) {
            cy.closeNotification('.cvat-notification-notice-load-settings-fail');
        }
    });
});

Cypress.Commands.add('cvat_userRegistration', (firstName, lastName, userName, emailAddr, password) => {
    cy.get('#firstName').type(firstName);
    cy.get('#lastName').type(lastName);
    cy.get('#username').type(userName);
    cy.get('#email').type(emailAddr);
    cy.get('#password1').type(password);
    cy.get('#password2').type(password);
    cy.get('.register-form-button').click();
    if (Cypress.browser.family === 'chromium') {
        cy.url().should('include', '/tasks');
    }
});

Cypress.Commands.add('goToTaskList', () => {
    cy.get('a[value="tasks"]').click();
    cy.url().should('include', '/tasks');
});

Cypress.Commands.add(
    'createAnnotationTask',
    (
        taskName = 'New annotation task',
        labelName = 'Some label',
        image = 'image.png',
        expectedResult = 'success',
    ) => {
        cy.get('#cvat-create-task-button').click({ force: true });
        cy.url().should('include', '/tasks/create');
        cy.get('[id="name"]').type(taskName);
        cy.get('.cvat-constructor-viewer-new-item').click();
        cy.get('[placeholder="Label name"]').type(labelName);
        cy.contains('button', 'Done').click();
        cy.get('input[type="file"]').attachFile(image, { subjectType: 'drag-n-drop' });

        cy.contains('Advanced configuration').click();
        cy.findByText(/^CVAT for video 1.1$/).click();
        cy.get('div[title="COCO 1.0"]').click();

        cy.contains('button', 'Submit').click();
        if (expectedResult === 'success') {
            cy.get('.cvat-notification-create-task-success').should('exist').find('[data-icon="close"]').click();
        }
        cy.goToTaskList();
    },
);

Cypress.Commands.add('openTask', (taskName, projectSubsetFieldValue) => {
    cy.contains('strong', taskName).parents('.cvat-tasks-list-item').contains('a', 'Open').click({ force: true });
    cy.get('.cvat-task-details').should('exist');
    if (projectSubsetFieldValue) {
        cy.get('.cvat-project-subset-field').find('input').should('have.attr', 'value', projectSubsetFieldValue);
    }
});

Cypress.Commands.add('saveJob', (method = 'PATCH', status = 200, as = 'saveJob') => {
    cy.intercept(method, `http://localhost/cvat-annotation/api/v1/jobs/**`).as(as);
    cy.get('button').contains('Save').click({ force: true });
    cy.wait(`@${as}`).its('response.statusCode').should('equal', status);
});

Cypress.Commands.add('openJob', (removeAnnotations = true, expectedFail = false) => {
    cy.get('.cvat-task-jobs-table')
        .contains(/^0-/)
        .parents('.cvat-task-jobs-table-row')
        .find('td')
        .find('a')
        .click()
    cy.url().should('include', '/jobs');
    if (expectedFail) {
        cy.get('.cvat-canvas-container').should('not.exist');
    } else {
        cy.get('.cvat-canvas-container').should('exist');
    }
    if (removeAnnotations) {
        cy.document().then((doc) => {
            const objects = Array.from(doc.querySelectorAll('.cvat_canvas_shape'));
            if (typeof objects !== 'undefined' && objects.length > 0) {
                cy.removeAnnotations();
                cy.saveJob('PUT');
            }
        });
    }
});

Cypress.Commands.add('openTaskJob', (taskName, removeAnnotations = true, expectedFail = false) => {
    cy.openTask(taskName);
    cy.openJob(removeAnnotations, expectedFail);
});

Cypress.Commands.add('interactControlButton', (objectType) => {
    cy.get('body').trigger('mousedown');
    cy.get(`.cvat-${objectType}-control`).trigger('mouseover');
    cy.get(`.cvat-${objectType}-popover`)
        .should('be.visible')
        .should('have.attr', 'style')
        .should('not.include', 'pointer-events: none');
});

Cypress.Commands.add('switchLabel', (labelName, objectType) => {
    cy.get(`.cvat-${objectType}-popover`).find('.ant-select-selection-item').click();
    cy.get('.ant-select-dropdown')
        .not('.ant-select-dropdown-hidden')
        .find(`.ant-select-item-option[title="${labelName}"]`)
        .click();
});

Cypress.Commands.add('checkPopoverHidden', (objectType) => {
    cy.get(`.cvat-${objectType}-popover`).should('be.hidden');
});

Cypress.Commands.add('checkObjectParameters', (objectParameters, objectType) => {
    const listCanvasShapeId = [];
    cy.document().then((doc) => {
        const listCanvasShape = Array.from(doc.querySelectorAll('.cvat_canvas_shape'));
        for (let i = 0; i < listCanvasShape.length; i++) {
            listCanvasShapeId.push(listCanvasShape[i].id.match(/\d+$/));
        }
        const maxId = Math.max(...listCanvasShapeId);
        cy.get(`#cvat_canvas_shape_${maxId}`).should('be.visible');
        cy.get(`#cvat-objects-sidebar-state-item-${maxId}`)
            .should('contain', maxId)
            .and('contain', `${objectType} ${objectParameters.type.toUpperCase()}`)
            .within(() => {
                cy.get('.ant-select-selection-item').should('have.text', selectedValueGlobal);
            });
    });
});

Cypress.Commands.add('createRectangle', (createRectangleParams) => {
    cy.interactControlButton('draw-rectangle');
    cy.switchLabel(createRectangleParams.labelName, 'draw-rectangle');
    cy.get('.cvat-draw-rectangle-popover').within(() => {
        cy.get('.ant-select-selection-item').then(($labelValue) => {
            selectedValueGlobal = $labelValue.text();
        });
        cy.contains('.ant-radio-wrapper', createRectangleParams.points).click();
        cy.contains('button', createRectangleParams.type).click();
    });
    cy.get('.cvat-canvas-container')
        .click(createRectangleParams.firstX, createRectangleParams.firstY)
        .click(createRectangleParams.secondX, createRectangleParams.secondY);
    if (createRectangleParams.points === 'By 4 Points') {
        cy.get('.cvat-canvas-container')
            .click(createRectangleParams.thirdX, createRectangleParams.thirdY)
            .click(createRectangleParams.fourthX, createRectangleParams.fourthY);
    }
    cy.checkPopoverHidden('draw-rectangle');
    cy.checkObjectParameters(createRectangleParams, 'RECTANGLE');
});

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
