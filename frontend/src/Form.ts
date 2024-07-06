import {acceptButton} from "./AcceptButton.ts";
import {FileInputBlock} from "./AddBlock.ts";

const fileInputBlock2:FileInputBlock = new FileInputBlock({ id: "file-input-2", description: "до 100мб", buttonText: "Загрузить ZIP файл Фотографий" });

export class Form{



    static return(){
        return `
                    <form id="add-form">
            ${fileInputBlock2.render()}
            ${acceptButton}
            </form>
        `
    }

    static addEventListeners():void{
        const form: HTMLFormElement = document.getElementById('add-form') as HTMLFormElement;



        const sumbitButton = document.querySelector('.button-accept')
        sumbitButton.addEventListener("click", (event) =>{

            event.preventDefault()
            const formData = new FormData(form)
            if (formData.get('file').size != 0){
            const res =  fetch("",{
                method: 'POST',
                body: formData,
            })}
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