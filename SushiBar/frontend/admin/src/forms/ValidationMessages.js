export const GetMessages = (elem) => {
  const messages = [];
  if (elem.validity.valueMissing) {
    messages.push("Potrzebna wartość!");
  }
  if (elem.validity.typeMismatch) {
    messages.push(`Nieprawidłowa wartość typu ${elem.type}`);
  }
  return messages;
}