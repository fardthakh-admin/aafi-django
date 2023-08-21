fetch('/api/patients/')
.then((resp) => resp.json())
.then((patients) => {
    const tableBody = document.getElementById('table-body');
    for(let patient of patients){
        
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
          <td scope="row" class="text-primary" ><a href="#">${patient.username}</a></td>
          <td>${patient.last_name}</td>
          <td>${patient.DOB}</td>
          <td>${patient.gender}</td>
          <td>${patient.email}</td>
          <td>${patient.phone_number}</td>
        `;

        tableBody.appendChild(newRow);
    }
})