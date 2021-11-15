
document.getElementById("submit-btn").addEventListener("click", async () => {
    var data = {
        username: document.getElementById("username-input").value,
        password: document.getElementById("password-input").value
    }
    
    if (!data.username || !data.password) {
        let errorText = document.getElementById("error-text");
        errorText.innerHTML = "Username and password are required";

        if (errorText.classList.contains("error--hidden")) {
            errorText.classList.remove("error--hidden");
        }
    } else {
        await fetch("/set-user-reg-details", {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json'
            },
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            body: JSON.stringify(data)
        });
        
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = "/register";
        document.body.appendChild(a);
        a.click();
    }
});
