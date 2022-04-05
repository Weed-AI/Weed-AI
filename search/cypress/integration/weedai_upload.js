describe('overall upload workflow', () => {

    beforeEach(() => {
        const test_username = `test_${Math.random().toString(36).slice(-4)}`
        // cvat requires at least one number in passwords
        const test_password = `P${Math.random().toString(36).slice(-8) + Math.random().toString().slice(-2)}`
        const test_email = `${test_username}@weed-ai.com`
        cy.wrap(test_username).as('test_username')
        cy.wrap(test_password).as('test_password')
        cy.wrap(test_email).as('test_email')
        cy.visit('http://localhost/upload', {failOnStatusCode: false})
        cy.register(test_username, test_email, test_password)
        cy.login(test_username, test_password)
        cy.findAllByRole('button', 'BEGIN UPLOAD').should('have.length', 1)
    })

    it('Test Weedcoco Upload', () => {
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /WeedCOCO/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_weedcoco/weedcoco.json')
        cy.clickText(/^Next$/)
        cy.get('div.fileContainer > input').attachFile('test_weedcoco/images/001_image.png')
        cy.clickText(/^Submit$/)
    })

    it('Test Weedcoco Zip Upload', () => {
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /WeedCOCO/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_weedcoco_zip/weedcoco.json')
        cy.clickText(/^Next$/)
        cy.findAllByText(/^Upload Image Files$/).click()  // select other option in dropdown
        cy.findAllByText(/^Upload Images in Zip$/).click()
        cy.get('input.uppy-Dashboard-input').attachFile('test_weedcoco_zip/weedcoco.zip')
        cy.wait(2000)
        cy.clickText(/^Submit$/)
    })

    it('Test Coco Upload', () => {
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /MS COCO/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_coco/coco.json')
        cy.clickText(/^Next$/)
        cy.findByText("crop").type('weed{enter}')
        cy.findByDisplayValue(/^UNSPECIFIED$/).click().clear().type('rapistrum rugosum{enter}')
        cy.clickText(/^Next$/)
        cy.setAgAndMeta()
        cy.get('div.fileContainer > input').attachFile('test_coco/images/002_image.png')
        cy.clickText(/^Submit$/)
    })

    it('Test Voc Upload', () => {
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /VOC/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.dzu-input').attachFile('test_voc/voc/resizeC1_PLOT_20190728_175852.xml')
        cy.get('.dzu-input').attachFile('test_voc/voc/resizeC1_PLOT_20190728_180135.xml')
        cy.get('.dzu-submitButton').click()
        cy.clickText(/^Next$/)
        cy.clickText(/^Next$/)
        cy.setAgAndMeta()
        cy.get('div.fileContainer > input').attachFile('test_voc/images/resizeC1_PLOT_20190728_175852.jpg')
        cy.get('div.fileContainer > input').attachFile('test_voc/images/resizeC1_PLOT_20190728_180135.jpg')
        cy.clickText(/^Submit$/)
    })

    it('Test Cvat Upload', function() {
        const label = 'weed: UNSPECIFIED'

        const task = {
            name: `task_${Math.random().toString(36).slice(-4)}`,
            label: label,
            image: 'test_cvat/003_image.jpg',
            createRectangleShape2Points: {
                points: 'By 2 Points',
                type: 'Shape',
                labelName: label,
                firstX: 250,
                firstY: 350,
                secondX: 350,
                secondY: 450,
            }
        }

        cy.visit('http://localhost/cvat-annotation/auth/register', {failOnStatusCode: false})
        cy.get('#firstName', { timeout: 60000 }).should('be.visible')
        cy.cvat_userRegistration('cvat_firstname', 'cvat_lastname', this.test_username, this.test_email, this.test_password)
        // cy.cvat_login(cvat_username, cvat_password)

        cy.createAnnotationTask(task.name, task.label, task.image)
        cy.openTaskJob(task.name)
        cy.createRectangle(task.createRectangleShape2Points)
        cy.saveJob()
        cy.wait(3000)

        cy.clearCookie('weedai_sessionid')        
        cy.visit('http://localhost/upload', {failOnStatusCode: false})
        cy.wait(3000)

        cy.login(this.test_username, this.test_password) 
        cy.clickText(/^Begin upload$/)
        cy.findByRole('dialog').findByRole('option', {name: /Annotation Project/i}).click()
        cy.clickText(/^Next$/)
        cy.get('.MuiAutocomplete-endAdornment').click()
        cy.findAllByText(task.name).first().click()
        cy.findAllByText(/^Apply$/).first().should('not.be.disabled', { timeout: 3000})
        cy.wait(5000)
        cy.findAllByText(/^Apply$/).first().should('not.be.disabled', { timeout: 3000})
        cy.wait(5000)
        // very bad but I don't understand why the first couple of clicks fail in cypress
        cy.clickText(/^Apply$/)
        cy.wait(5000)
        cy.clickText(/^Apply$/)
        cy.wait(5000)
        cy.clickText(/^Apply$/)
        cy.wait(5000)
        cy.clickText(/^Next$/)
        cy.findByText(task.label.split(': ')[0]).type('weed{enter}')
        cy.findByDisplayValue(task.label.split(': ')[1]).click().clear().type('rapistrum rugosum{enter}')
        cy.clickText(/^Next$/)
        cy.setAgAndMeta()
        cy.clickText(/^Submit$/)
    })

    afterEach(() => {
        cy.wait(1000)
        cy.findAllByText(/^Log out$/).should('have.length', 1).click()
    })
})
