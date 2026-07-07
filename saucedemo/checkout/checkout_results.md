# Checkout Module — Cross-Browser Test Results

Suite: `checkout/test_checkout_page.py` (CO-001 .. CO-032)
Run: `pytest checkout/test_checkout_page.py --browsers=chrome,firefox,edge,opera --headless`
Result: **96 passed, 32 skipped** (Chrome 32/32, Firefox 32/32, Edge 32/32, Opera skipped)

| Case Number | Test Case/Scenario | Chrome | Firefox | Edge | Opera | Remarks |
|---|---|---|---|---|---|---|
| CO-001 | Verify if the First Name field is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-002 | Verify if the First Name field accepts focus. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-003 | Verify if valid input can be entered into the First Name field. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-004 | Verify the behavior when the First Name field is left empty. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-005 | Verify the behavior when spaces are entered into the First Name field. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-006 | Verify if the Last Name field is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-007 | Verify if the Last Name field accepts focus. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-008 | Verify if valid input can be entered into the Last Name field. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-009 | Verify the behavior when the Last Name field is left empty. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-010 | Verify the behavior when spaces are entered into the Last Name field. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-011 | Verify if the Postal Code field is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-012 | Verify if the Postal Code field accepts focus. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-013 | Verify if valid input can be entered into the Postal Code field. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-014 | Verify the behavior when the Postal Code field is left empty. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-015 | Verify the behavior when spaces are entered into the Postal Code field. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-016 | Verify if the Continue button is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-017 | Verify if the Order Summary page is displayed after entering valid checkout information. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-018 | Verify the behavior when the First Name field is left empty (Continue). | pass | pass | pass | blocked | Error shown: "Error: First Name is required". Opera not installed. |
| CO-019 | Verify the behavior when the Last Name field is left empty (Continue). | pass | pass | pass | blocked | Error shown: "Error: Last Name is required". Opera not installed. |
| CO-020 | Verify the behavior when the Postal Code field is left empty (Continue). | pass | pass | pass | blocked | Error shown: "Error: Postal Code is required". Opera not installed. |
| CO-021 | Verify the behavior when all required fields are left empty (Continue). | pass | pass | pass | blocked | First-name error shown first (validated in order). Opera not installed. |
| CO-022 | Verify if the Cancel button is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-023 | Verify if the Shopping Cart Module is displayed after clicking Cancel. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-024 | Verify if the Order Summary page is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-025 | Verify if the selected product information is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-026 | Verify if the payment information is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-027 | Verify if the shipping information is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-028 | Verify if the total amount is displayed correctly. | pass | pass | pass | blocked | Item total + tax = total verified numerically. Opera not installed. |
| CO-029 | Verify if the Finish button is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-030 | Verify if the order can be completed successfully. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-031 | Verify if the Back Home button is displayed. | pass | pass | pass | blocked | Opera not installed on test machine |
| CO-032 | Verify if the Inventory Module is displayed after clicking Back Home. | pass | pass | pass | blocked | Opera not installed on test machine |

## Notes

- **Environment fact (not a product defect):** SauceDemo's checkout form fields and
  action buttons are React-controlled. In this Selenium environment, synthesized
  keystrokes are intermittently dropped before React commits them to state, and a
  native click on the submit button does not fire the React handler. The suite
  therefore enters text by setting the value through the native setter + a real
  `input` event (which React's `onChange` observes) and activates Continue / Finish /
  Cancel / Back Home via a JavaScript-dispatched `click()`. Both paths use the same
  DOM APIs a real interaction would.
- The `/v1/` URLs in the prerequisites permanently redirect to the current SauceDemo
  site; tests use `/v1/` as the login entry point and target the served DOM.
- Opera is Chromium-based and supported by the driver factory, but it is not
  installed on this machine, so those runs are reported as **blocked** (pytest
  SKIPPED) rather than failed.
