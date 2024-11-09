import React, { useState, useEffect } from 'react';

export function MenuPage(props) {
    const [showSpan, setShowSpan] = useState(false);

    useEffect(() => {
        //console.log("MenuPage")
        //return () => console.log("Funkcja useEffect")
    });

    const handleClick = (event) => {
        setShowSpan(!showSpan);
        //props.callback(event);
    }

    const getMessageElement = () => {
        let div = <div id={"messageDiv"} className={"h5 text-center p-2"}>
            {props.message}
        </div>
        return showSpan ? <span>{div}</span> : div;
    }

    return(
        <div>
            <button onClick={handleClick}>asd</button>
            {getMessageElement()}
        </div>
    )
}