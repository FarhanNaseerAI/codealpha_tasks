/**
 * Credit Scoring Application JavaScript
 * Form Validation, Spinner Overlay, Quick Demo Profiles
 */

document.addEventListener('DOMContentLoaded', () => {
    const creditForm = document.getElementById('creditForm');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const submitBtn = document.getElementById('submitBtn');
    const alertBox = document.getElementById('clientAlert');

    if (creditForm) {
        creditForm.addEventListener('submit', (event) => {
            // Reset previous field errors
            clearFieldValidationErrors();
            showAlert('', false);

            let isValid = true;
            const requiredInputs = creditForm.querySelectorAll('input[required], select[required]');

            requiredInputs.forEach(input => {
                const value = input.value.trim();
                const fieldName = input.getAttribute('data-name') || input.name;

                if (!value) {
                    isValid = false;
                    markFieldInvalid(input, `${fieldName} is required.`);
                } else if (input.type === 'number') {
                    const numVal = parseFloat(value);
                    const min = input.getAttribute('min') !== null ? parseFloat(input.getAttribute('min')) : null;
                    const max = input.getAttribute('max') !== null ? parseFloat(input.getAttribute('max')) : null;

                    if (isNaN(numVal)) {
                        isValid = false;
                        markFieldInvalid(input, `Please enter a valid number for ${fieldName}.`);
                    } else if (min !== null && numVal < min) {
                        isValid = false;
                        markFieldInvalid(input, `${fieldName} must be at least ${min}.`);
                    } else if (max !== null && numVal > max) {
                        isValid = false;
                        markFieldInvalid(input, `${fieldName} cannot exceed ${max}.`);
                    }
                }
            });

            if (!isValid) {
                event.preventDefault();
                showAlert('Please fix highlighted errors in the form before submitting.', true);
                const firstInvalid = creditForm.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
                return;
            }

            // Form is valid - show loading spinner overlay and disable button
            if (loadingOverlay) {
                loadingOverlay.style.display = 'flex';
            }
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin me-2"></i> Analyzing Profile...';
            }
        });
    }

    function markFieldInvalid(inputElement, errorMsg) {
        inputElement.classList.add('is-invalid');
        const parent = inputElement.closest('.form-group') || inputElement.parentElement;
        let feedback = parent.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback d-block text-danger small mt-1';
            parent.appendChild(feedback);
        }
        feedback.innerText = errorMsg;
    }

    function clearFieldValidationErrors() {
        if (!creditForm) return;
        const invalidFields = creditForm.querySelectorAll('.is-invalid');
        invalidFields.forEach(el => el.classList.remove('is-invalid'));

        const feedbacks = creditForm.querySelectorAll('.invalid-feedback');
        feedbacks.forEach(el => el.remove());
    }

    function showAlert(message, show = true) {
        if (!alertBox) return;
        if (show) {
            alertBox.innerText = message;
            alertBox.classList.remove('d-none');
        } else {
            alertBox.classList.add('d-none');
        }
    }
});

/**
 * Quick Fill Demo Profile Helper
 * Automatically populates input fields with synthetic profiles for quick testing
 */
function fillDemoProfile(profileType) {
    const profiles = {
        'good': {
            'Age': 42,
            'Annual_Income': 120000,
            'Monthly_Inhand_Salary': 9500,
            'Num_Bank_Accounts': 3,
            'Num_Credit_Cards': 4,
            'Interest_Rate': 6,
            'Num_of_Loan': 1,
            'Delay_from_due_date': 2,
            'Num_of_Delayed_Payment': 0,
            'Changed_Credit_Limit': 12.5,
            'Num_Credit_Inquiries': 1,
            'Credit_Mix': 'Good',
            'Outstanding_Debt': 450,
            'Credit_Utilization_Ratio': 24.5,
            'Credit_History_Age_Months': 210,
            'Payment_of_Min_Amount': 'Yes',
            'Total_EMI_per_month': 350,
            'Amount_invested_monthly': 600,
            'Payment_Behaviour': 'High_spent_Large_value_payments',
            'Monthly_Balance': 1850
        },
        'standard': {
            'Age': 31,
            'Annual_Income': 52000,
            'Monthly_Inhand_Salary': 4100,
            'Num_Bank_Accounts': 5,
            'Num_Credit_Cards': 6,
            'Interest_Rate': 14,
            'Num_of_Loan': 3,
            'Delay_from_due_date': 12,
            'Num_of_Delayed_Payment': 4,
            'Changed_Credit_Limit': 8.0,
            'Num_Credit_Inquiries': 5,
            'Credit_Mix': 'Standard',
            'Outstanding_Debt': 1800,
            'Credit_Utilization_Ratio': 38.2,
            'Credit_History_Age_Months': 96,
            'Payment_of_Min_Amount': 'Yes',
            'Total_EMI_per_month': 520,
            'Amount_invested_monthly': 180,
            'Payment_Behaviour': 'Low_spent_Medium_value_payments',
            'Monthly_Balance': 640
        },
        'poor': {
            'Age': 24,
            'Annual_Income': 19000,
            'Monthly_Inhand_Salary': 1450,
            'Num_Bank_Accounts': 8,
            'Num_Credit_Cards': 9,
            'Interest_Rate': 28,
            'Num_of_Loan': 7,
            'Delay_from_due_date': 38,
            'Num_of_Delayed_Payment': 18,
            'Changed_Credit_Limit': 2.0,
            'Num_Credit_Inquiries': 14,
            'Credit_Mix': 'Bad',
            'Outstanding_Debt': 4800,
            'Credit_Utilization_Ratio': 49.5,
            'Credit_History_Age_Months': 18,
            'Payment_of_Min_Amount': 'No',
            'Total_EMI_per_month': 890,
            'Amount_invested_monthly': 20,
            'Payment_Behaviour': 'Low_spent_Small_value_payments',
            'Monthly_Balance': 85
        }
    };

    const selected = profiles[profileType];
    if (!selected) return;

    for (const [key, val] of Object.entries(selected)) {
        const input = document.getElementsByName(key)[0];
        if (input) {
            input.value = val;
            input.classList.remove('is-invalid');
        }
    }
}
