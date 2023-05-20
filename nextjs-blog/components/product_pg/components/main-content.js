import Project from "./project"
import st from "../../../styles/product_pg/main_content.module.css"
import * as Separator from '@radix-ui/react-separator';

export default function MainContent(props){
    let company_obj = props.company_obj
    let contractor_obj = props.contractor_obj
    // let project_cards = obj.projects.map( (x) => <Project project = {x} /> ) 


    

    return(

        // {
        //     about_us : "", 
        //     company_name : "", 
        //     contractor_name : "", 
        //     phone_no : "", 
        //     website : "", 
        //     address : ""
        //    }
        
        <div className={st.main_content}>
            <header>
                <nav className={st.nav}>
                    <a href="#aboutus">About Us</a>
                    <a href="#business">Business</a>
                </nav>
            </header>

            <Separator.Root className={st.SeparatorRoot} style={{ margin: '15px 0' }} />
            <div className={st.about_us} id = "aboutus">
                <div className={st.heading}>
                    About Us
                </div>
                <div className={st.greybg}>
                    {company_obj.about_us}
                </div>
                
            </div>

            <Separator.Root className={st.SeparatorRoot} style={{ margin: '15px 0' }} />

            <div id = "business" className={st.business_details}>
            <div className={st.heading}>
                    Business 
            </div>
            <div className={st.business_container}>
                <div className={st.business_item}>
                    <label className={st.business_label}>
                        Business Name
                    </label>
                    <div className={st.business_text}>
                        {company_obj.company_name} 
                    </div>
                </div>
                
                <div className={st.business_item}></div>
                    <label className={st.business_label}>
                        Phone Number
                    </label>
                    <div className={st.business_text}>
                        {contractor_obj.phone_no} 
                    </div>
                </div>
                
                <div className={st.business_item}>
                    <label className={st.business_label}>
                        Website
                    </label>
                    <div className={st.website_link}>
                        <a href={company_obj.website} >
                        {company_obj.website}
                        </a>
                    </div>
                </div>

                <div className={st.business_item}>
                    <label className={st.business_label}>
                        Address
                    </label>
                    <div className={st.business_text}>
                        {contractor_obj.address} 
                    </div>
                </div>


            </div>

            
            {/* <Separator.Root className={st.SeparatorRoot} style={{ margin: '15px 0' }} /> 

            <div className={st.reviews}>
                <div className={st.review_btn} >
                    <button className={st.btn} onClick={review_handler}>Add Review</button>
                </div>
            </div> */}

            {/* <Footer />  */}

        </div>
        
    )
}