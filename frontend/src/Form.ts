import {acceptButton} from "./AcceptButton.ts";
import {FileInputBlock} from "./AddBlock.ts";

export const fileInputBlock1:FileInputBlock = new FileInputBlock({ id: "file-input-1", description: "до 100мб", buttonText: "Загрузить ZIP файл Фотографий" });

export class Form{


     return(){
        return `
            <form id="add-form">
            ${fileInputBlock1.render()}
            ${acceptButton}
            </form>
        `
    }

    addEventListeners():void{
        const form: HTMLFormElement = document.getElementById('add-form') as HTMLFormElement;



        const sumbitButton = document.querySelector('.button-accept')
        sumbitButton.addEventListener("click", (event) =>{

            event.preventDefault()

            const inputElement = document.querySelector(`#${fileInputBlock1.getId()}`) as HTMLInputElement;
            const file = inputElement.files[0]
            const formData = new FormData()
            formData.append("zip_file", file )
            if (formData.get('zip_file').size != 0) {
                const res = fetch("http://localhost/api/upload-zip-file", {
                    method: 'POST',
                    body: formData,
                }).then(res => {
                    return res.text().then(text => {
                        return {
                            status: res.status,
                            ok: res.ok,
                            text: text
                        };
                    });
                })
                    .then(res => {
                        if (res.ok) {
                            const data = JSON.parse(res.text);
                            console.log(data);
                        } else {
                            console.error('Ошибка при загрузке файла:', res.status, res.text);
                        }
                    })
                    .catch(error => {
                        console.error('Произошла ошибка:', error);
                    })
            }
            else {
                const cardBlock = document.querySelector('.card-block')
                cardBlock.style.border = "1px solid #ff0404"
                cardBlock.style.boxShadow = "0 0 15px 0 rgba(255, 1, 1, 0.25)"

                setTimeout(() =>{

                    cardBlock.style.border = "1px solid #d4d4d4"
                    cardBlock.style.boxShadow = "none"
                }, 1000)
            }
        })
    }
}