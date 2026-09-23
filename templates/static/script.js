async function translateText() {

    const text = document.getElementById("inputText").value.trim();
    const source = document.getElementById("sourceLanguage").value;
    const target = document.getElementById("targetLanguage").value;
    const output = document.getElementById("outputText");

    if (text === "") {
        output.textContent = "Please enter some text first.";
        return;
    }

    output.textContent = "Translating... ⏳";

    try {
        const response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                source: source,
                target: target
            })
        });

        const data = await response.json();

        if (data.translation) {
            output.textContent = data.translation;
        } else {
            output.textContent = data.error || "Translation failed.";
        }

    } catch (error) {
        console.error(error);
        output.textContent =
            "Unable to connect to translation service.";
    }
}