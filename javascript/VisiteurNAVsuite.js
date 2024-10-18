

let selectedOptions = {
    grade: null,
    diplome: null,
    etablissement: null,
    sexe: null
    
};

function show(Explorer) {
    selectedOptions.Explorer = (selectedOptions.Explorer=== Explorer) ? null : Explorer;
    document.querySelector('.filtrex .textBox2').value = selectedOptions.Explorer ? Explorer : '';
}


let dropdown2s = document.querySelectorAll('.dropdown2');

dropdown2s.forEach(dropdown2 => {
    let menuIcon2 = dropdown2.querySelector('.menu-icon2');

    dropdown2.onclick = function() {
        menuIcon2.classList.toggle('active');
        dropdown2.classList.toggle('active');
    };
});

  
let dropdowns = document.querySelectorAll('.dropdown');

dropdowns.forEach(dropdown => {
    let menuIcon = dropdown.querySelector('.menu-icon');

    dropdown.onclick = function() {
        menuIcon.classList.toggle('active');
        dropdown.classList.toggle('active');
    };
});



function showGrade(grade) {
    selectedOptions.grade = (selectedOptions.grade === grade) ? null : grade;
    document.querySelector('.filtre1 .textBox').value = selectedOptions.grade ? grade : '';
}

function showDiplome(diplome) {
    selectedOptions.diplome = (selectedOptions.diplome === diplome) ? null : diplome;
    document.querySelector('.filtre2 .textBox').value = selectedOptions.diplome ? diplome : '';
}

function showEtablissement(etablissement) {
    selectedOptions.etablissement = (selectedOptions.etablissement === etablissement) ? null : etablissement;
    document.querySelector('.filtre3 .textBox').value = selectedOptions.etablissement ? etablissement : '';
}

function showSexe(sexe) {
    selectedOptions.sexe = (selectedOptions.sexe === sexe) ? null : sexe;
    document.querySelector('.filtre4 .textBox').value = selectedOptions.sexe ? sexe : '';
}

 document.addEventListener("DOMContentLoaded", function() {
         const form = document.querySelector('.partie-recherche form');
         const resultList = document.querySelector('.publication-list');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche le formulaire de se soumettre normalement

        const searchQuery = document.querySelector('.rechercher').value.trim();

        // Envoi de la requête AJAX avec Fetch
        fetch(`http://127.0.0.1:8000/api/chercheur-generalesearch/?q=${searchQuery}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                //'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0NjUyNjUyLCJpYXQiOjE3MTQ2NTIwNTIsImp0aSI6IjMyZjYzZWVhYTgxZTQ5YjlhOGNjMGVhODUwZDVjNGZiIiwidXNlcl9pZCI6MjJ9.NUz3cEKX79BrCyc-93c0abq6EAbeB9Ma6KHLVGEV6_k'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {




           if (data.length === 0) {
                // No results found, redirect to notFound.html
                window.location.href = 'file:///C:/Users/ASUS%20TUF%20A15/PycharmProjects/Auth2/front/html/notFound1.html';
            } else {
               resultList.innerHTML = '';



            // Boucle à travers les résultats et les affiche sur la page
            data.forEach(item => {
                const chercheurHTML = `
                    <li>
                        <span><img class="profil-pic" src="../images/user profil.png" alt="profil chercheur" /></span>
                        <span class="nom">${item.nom_chercheur} ${item.prenom_chercheur}</span>
                        <span>${item.grade_ensignement}</span>
                        <span>${item.email}</span>
                        <span>${item.equipe}</span>
                        <span class="more" onclick="redirectToDetails('${item.detail_url}')">details</span>
                    </li>
                `;
                resultList.insertAdjacentHTML('beforeend', chercheurHTML);
            });
             }
        })
        .catch(error => {
           console.error('Error fetching data:', error);
   window.location.href = 'file:///C:/Users/ASUS%20TUF%20A15/PycharmProjects/Auth2/front/html/notFound1.html';
        });
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('.partie-recherche form');
    const resultList = document.querySelector('.publication-list');
    const filterButton = document.querySelector('.button-filtrer');

    filterButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally

        const searchQuery = document.querySelector('.rechercher').value.trim();

        // Retrieve selected values from filters
        const gradeEnseignement = document.querySelector('.filtre1 .textBox').value.trim();
        const diplome = document.querySelector('.filtre2 .textBox').value.trim();
        const etablissement = document.querySelector('.filtre3 .textBox').value.trim();
        const sexe = document.querySelector('.filtre4 .textBox').value.trim();

        // Send AJAX request using Fetch
        fetch(`http://127.0.0.1:8000/api/chercheur-search/?q=${searchQuery}&grade_ensignement=${gradeEnseignement}&diplome=${diplome}&etablissement=${etablissement}&sexe=${sexe}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
               // 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE0NjU0MDQwLCJpYXQiOjE3MTQ2NTM0NDAsImp0aSI6ImRjOTE3YjlmZWMyZTQ2MTZiY2UxZWQxMDE2NjhiMmViIiwidXNlcl9pZCI6MjJ9.fqRA7HMCYq5Eg1tbPuhtBa6Ba_4HHVm87rru-B3QW1Y'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {



             if (data.length === 0) {
                // No results found, redirect to notFound.html
                window.location.href = 'file:///C:/Users/ASUS%20TUF%20A15/PycharmProjects/Auth2/front/html/notFound1.html';
            } else {
                 resultList.innerHTML = '';
            // Loop through the results and display them on the page
            data.forEach(item => {
                const chercheurHTML = `
                    <li>
                        <span><img class="profil-pic" src="../images/user profil.png" alt="profil chercheur" /></span>
                        <span class="nom">${item.nom_chercheur} ${item.prenom_chercheur}</span>
                        <span>${item.grade_ensignement}</span>
                        <span>${item.email}</span>
                        <span>${item.equipe}</span>
                        <span class="more" onclick="redirectToDetails('${item.detail_url}')">details</span>
                    </li>
                `;
                resultList.insertAdjacentHTML('beforeend', chercheurHTML);
            });
            }
        })
        .catch(error => {
     console.error('Error fetching data:', error);
     window.location.href = 'file:///C:/Users/ASUS%20TUF%20A15/PycharmProjects/Auth2/front/html/notFound1.html';
        });
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const resultList = document.querySelector('.publication-list');

    // Fetch pour récupérer les données de l'API
    fetch('http://127.0.0.1:8000/api/chercheurs/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            // Autres en-têtes requis, par exemple pour l'authentification
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Votre code pour générer dynamiquement la liste des chercheurs à partir des données récupérées
        // Par exemple :
        resultList.innerHTML = ''; // Effacer le contenu précédent de la liste
        data.forEach(item => {
            const chercheurHTML = `
                <li>
                    <span><img class="profil-pic" src="../images/user profil.png" alt="profil chercheur" /></span>
                    <span class="nom">${item.nom_chercheur} ${item.prenom_chercheur}</span>
                    <span>${item.grade_ensignement}</span>
                    <span>${item.email}</span>
                    <span>${item.equipe}</span>
                    <span class="more" onclick="redirectToDetails('${item.detail_url}')">details</span>
                </li>
            `;
            resultList.insertAdjacentHTML('beforeend', chercheurHTML);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        // Gérer les erreurs, par exemple afficher un message d'erreur à l'utilisateur
    });
});


function redirectToDetails(detailUrl) {
    const chercheurId = detailUrl.match(/\/(\d+)\/$/)[1]; // Extraire l'ID du chercheur à partir de l'URL
    sessionStorage.setItem('id_chercheur', chercheurId); // Stocker l'ID du chercheur dans la session
    window.location.href = '../html/voirprofilautrechercheur.html'; // Rediriger l'utilisateur vers une autre page
}