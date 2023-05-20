import st from "../../../styles/dashboard/card.module.css";
import { useRouter } from "next/router";

export default function Order(props) {
  let obj = props.obj;
  let router = useRouter();
  console.log("printing order");
  console.log(obj);
  let query_obj = {
    company_img_url: obj.company_img_url,
    product_img_url: obj.product_img_url,
    description: obj.description,
    contractor_id: obj.contractor_id,
    company_id: obj.company_id,
    category: obj.category,
    id: obj.p_uid,
  };

  return (
    <div
      className={st.card_container}
      onClick={() => router.push({ pathname: "/product_pg", query: query_obj })}
    >
      <div className={st.img}>
        <img src={obj.product_img_url} className={st.img2} />
      </div>

      <div className={st.details}>
        <div className={st.infocontainer}>
          <label htmlFor="companyname" className={st.label}>
            <strong>Company Name:</strong>
          </label>
          <span id="companyname" className={st.item}>
            {obj.company_name}
          </span>
        </div>

        <div className={st.infocontainer}>
          <label htmlFor="location" className={st.label}>
            <strong>Location:</strong>
          </label>
          <span id="location" className={st.item}>
            {obj.location}
          </span>
        </div>

        <div className={st.infocontainer}>
          <label htmlFor="category" className={st.label}>
            <strong>Category:</strong>
          </label>
          <span id="category" className={st.item}>
            {obj.category}
          </span>
        </div>

        <div className={st.infocontainer}>
          <label htmlFor="datetime" className={st.label}>
            <strong>Order Date:</strong>
          </label>
          <span id="datetime" className={st.item}>
            {obj.order_date_time}
          </span>
        </div>

        <div className={st.infocontainer}>
          <label htmlFor="companyname" className={st.label}>
            <strong>Message:</strong>
          </label>
          <span id="companyname" className={st.item}>
            {obj.message}
          </span>
        </div>
      </div>
    </div>
  );
}
