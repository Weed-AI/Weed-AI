import { useEffect, useState, useRef } from "react"

function useSticky() {
    const [isSticky, setSticky] = useState(false)
    const element = useRef(null)

    const handleScroll = () => {
        window.scrollY > element.current.getBoundingClientRect().bottom
            ? setSticky(true)
            : setSticky(false)
    }

    // This function handle the scroll performance issue
    const debounce = (func, wait = 20, immediate = true) => {
        let timeOut
        return () => {
            let context = this,
                args = arguments
            const later = () => {
                timeOut = null
                if (!immediate) func.apply(context, args)
            }
            const callNow = immediate && !timeOut
            clearTimeout(timeOut)
            timeOut = setTimeout(later, wait)
            if (callNow) func.apply(context, args)
        }
    }

    useEffect(() => {
        window.addEventListener("scroll", debounce(handleScroll))
        return () => {
            window.removeEventListener("scroll", () => handleScroll)
        }
    }, [debounce, handleScroll])

    return { isSticky, element }
}

export default useSticky