import { acceptButton } from "./AcceptButton.ts";
import { FileInputBlock } from "./AddBlock.ts";

export const fileInputBlock1: FileInputBlock = new FileInputBlock({ id: "file-input-1", description: "до 100мб", buttonText: "Загрузить ZIP файл Фотографий" });

export let data = null;

function injectData(data) {
    const Block = document.querySelector(".central_main-block");
    if (Block) {
        console.log(data)
        Block.insertAdjacentHTML('beforeend', `<h2>Результат</h2>`)
        for (const [fileName, fileData] of Object.entries(data)) {
            const base64Image = fileData[1];
            const html = `
                <div class="image-block">
                    <h5>${fileData[0]}</h5>
                    <img src="data:image/jpeg;base64,${base64Image}" alt="${fileName}" />
                </div>
            `;
            Block.insertAdjacentHTML('beforeend', html);
        }
    } else {
        console.error("Element .central_main-block not found");
    }
}


export class Form {
    return() {
        return `
            <form id="add-form">
                ${fileInputBlock1.render()}
                ${acceptButton}
            </form>
        `;
    }

    addEventListeners() {
        const form: HTMLFormElement = document.getElementById('add-form') as HTMLFormElement;
        const submitButton = document.querySelector('.button-accept');

        submitButton.addEventListener("click", (event) => {
            event.preventDefault();

            const inputElement = document.querySelector(`#${fileInputBlock1.getId()}`) as HTMLInputElement;
            const file = inputElement.files[0];
            console.log(file);

            const formData = new FormData();
            formData.append("zip_file", file);

            if (formData.get('zip_file').size != 0) {
                fetch("http://localhost/api/upload-zip-file", {
                    method: 'POST',
                    body: formData,
                })
                    .then(res => res.text().then(text => ({
                        status: res.status,
                        ok: res.ok,
                        text: text
                    })))
                    .then(res => {
                        if (res.ok) {
                            data = JSON.parse(res.text);
                            injectData(data);
                        } else {
                            console.error('Ошибка при загрузке файла:', res.status, res.text);
                        }
                    })
                    .catch(error => {
                        console.error('Произошла ошибка:', error);
                    });
            } else {
                const cardBlock = document.querySelector('.card-block');
                cardBlock.style.border = "1px solid #ff0404";
                cardBlock.style.boxShadow = "0 0 15px 0 rgba(255, 1, 1, 0.25)";

                setTimeout(() => {
                    cardBlock.style.border = "1px solid #d4d4d4";
                    cardBlock.style.boxShadow = "none";
                }, 1000);
            }
        });
    }
}