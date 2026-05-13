const person = {
    name: "Андрей",      
    age: 19,           
    hobbies: ["чтение", "спорт"],
    address: {          
      city: "Нижний Новгород",
      street: "Ленина"
    }
  };
  
  const getProperty = (obj, key) => {
    console.log(obj[key]);
  };
  
  getProperty(person, "name"); 
  getProperty(person, "hobbies"); 