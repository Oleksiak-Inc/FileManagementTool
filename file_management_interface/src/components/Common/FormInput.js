import React from 'react';
import './FormInput.css';

const FormInput = ({ label, type = 'text', value, onChange, placeholder, required = false, options = [] }) => {
    const renderInput = () => {
        switch (type) {
            case 'select':
                return (
                    <select
                        className="form-input"
                        value={value}
                        onChange={onChange}
                        required={required}
                    >
                        <option value="">Select {label}</option>
                        {options.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}
                            </option>
                        ))}
                    </select>
                );
            case 'textarea':
                return (
                    <textarea
                        className="form-input"
                        value={value}
                        onChange={onChange}
                        placeholder={placeholder}
                        required={required}
                        rows="4"
                    />
                );
            default:
                return (
                    <input
                        className="form-input"
                        type={type}
                        value={value}
                        onChange={onChange}
                        placeholder={placeholder}
                        required={required}
                    />
                );
        }
    };

    return (
        <div className="form-group">
            <label className="form-label">{label}</label>
            {renderInput()}
        </div>
    );
};

export default FormInput;