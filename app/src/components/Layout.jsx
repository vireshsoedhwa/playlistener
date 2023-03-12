import { Outlet } from "react-router-dom"

export default function Layout() {
    return (
        <div>
            {/* <h1>Layout component</h1> */}
            <Outlet />
        </div>
    )
}