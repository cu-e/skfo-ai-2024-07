import "./style.css";

type BlockProps = {
    id: string;
    description: string;
    buttonText: string;
};

export class FileInputBlock {
    id: string;
    description: string;
    buttonText: string;

    constructor({ id, description, buttonText }: BlockProps) {
        this.id = id;
        this.description = description;
        this.buttonText = buttonText;
    }
    public getId(){
        return this.id
    }

    render(): string {
        return `
      <input type="file" multiple accept=".zip" name="file" id="${this.id}">  
      <label for="${this.id}">
        <div class="card-block" >
          <svg width="72" height="72" viewBox="0 0 72 72" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 66H54C55.5913 66 57.1174 65.3679 58.2426 64.2426C59.3679 63.1174 60 61.5913 60 60V22.5L43.5 6H18C16.4087 6 14.8826 6.63214 13.7574 7.75736C12.6321 8.88258 12 10.4087 12 12V24" stroke="#545454" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M42 6V24H60" stroke="#545454" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M6 45H36" stroke="#545454" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
            <path d="M27 54L36 45L27 36" stroke="#545454" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <p class="discripttext" id="${this.id}-description">${this.description}</p>
          <p class="input-file-text">${this.buttonText}</p> 
        </div>
      </label>
    `;
    }

    addEventListeners(): void {
        const inputElement = document.querySelector(`#${this.id}`) as HTMLInputElement;
        inputElement?.addEventListener('change', (event) => {

            const nameElement:string = inputElement.files[0].name

            // console.log(nameElement)

            let sizeElement =  Number(inputElement.files[0].size / 1000 ** 2).toFixed(1)
            const descriptionElement = document.querySelector(`#${this.id}-description`);
            const inputElementText = document.querySelector(".input-file-text")
            const inputElementDom = document.querySelector(".card-block")
            if (descriptionElement) {
                descriptionElement.textContent = `${this.description} ( ${sizeElement} мб.)`;
                inputElementText.textContent = `Файл ${nameElement} выбран!`
                inputElementDom.style.background = "#F4F3FF"
            }
        });
    }
}
