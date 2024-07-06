export const acceptButton =
    `
    <style>
    .button-accept{
        border-radius: 12px;
        width: 500px;
        height: 40px;
        background: linear-gradient(146deg, #fec900 0%, #ffe631 100%);
        border: 0;
        cursor: pointer;
    }
    .button-accept:hover{
           transition: 300ms;
           background: linear-gradient(146deg, #ffe687 0%, #fff4a8 100%);
    }
    @media screen and (max-width: 700px) {
    .button-accept {
        width: calc(90vw - 30px);
    }
} 
    </style>
    <button class="button-accept" type="submit">Начать</button>
    `