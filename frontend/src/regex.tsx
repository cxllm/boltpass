// Regex to verify if an email is valid
const emailRegex =
	/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$/;
// Regex to verify if password is secure
const passwordRegex =
	/^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^0-9A-Za-z]).{8,}$/;
// Regexes to verify if individual things are present
const lowercaseRegex = /^.*[a-z]+.*$/;
const uppercaseRegex = /^.*[A-Z]+.*$/;
const numbersRegex = /^.*[0-9]+.*$/;
const specialCharsRegex = /^.*[^0-9A-Za-z]+.*$/;
export {
	emailRegex,
	passwordRegex,
	lowercaseRegex,
	uppercaseRegex,
	numbersRegex,
	specialCharsRegex
};
