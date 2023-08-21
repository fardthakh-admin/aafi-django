fetch('/api/patient-list/')
.then((resp) => resp.json())
.then((data) => {
    let itterable = 1;
    const tableBody = document.getElementById('table-body');
    for(let patient of data){
        if(itterable === 1){
            document.getElementById('record-number').innerText =itterable
            document.getElementById('patient-id').innerText = patient.id
            document.getElementById('patient-name').innerText = patient.username
            document.getElementById('patient-gender').innerText = patient.gender
            document.getElementById('patient-DOB').innerText = patient.DOB
        }
        else{
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
              <th scope="row" class="text-primary">${itterable}</th>
              <td>${patient.id}</td>
              <td>${patient.username}</td>
              <td>${patient.gender}</td>
              <td>${patient.DOB}</td>
            `;

            tableBody.appendChild(newRow);
        }
        itterable++
    }
})