document.addEventListener("DOMContentLoaded", async () => {
    const cluesList = document.getElementById("clues-list");

    try {
        const response = await fetch('/api/clues');
        if (!response.ok) {
            throw new Error("Erreur lors du chargement des indices");
        }

        const clues = await response.json();

        clues.forEach((clue, index) => {
            const listItem = document.createElement("li");
            listItem.textContent = `Indice ${index + 1} : ${clue}`;
            cluesList.appendChild(listItem);
        });
    } catch (error) {
        cluesList.innerHTML = `<li>Impossible de charger les indices : ${error.message}</li>`;
    }
});
