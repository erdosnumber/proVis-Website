import React from 'react';
import st from '../../../styles/listing_pg/card.module.css';
import { alertService } from '../../../services/alert.service';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../../redux/reducers';
import Spinner from '../../loader';
import config from 'config';
import { Alert } from 'antd';
import axios from 'axios';

export default function Card(props) {
  // ml api code
  let obj = props.obj;
  const [translationText, setTranslationText] = React.useState(obj.description);
  const [displayLang, setdisplayLang] = React.useState(0);
  const [loader, setLoader] = React.useState(false);

  const translateText = () => {
    let data = {
      q: translationText,
      source: displayLang == 0 ? 'en' : 'hi',
      target: displayLang == 0 ? 'hi' : 'en',
    };

    setLoader(true);
    axios.post(`https://libretranslate.de/translate`, data).then((response) => {
      setTranslationText(response.data.translatedText);
      console.log(response.data.translatedText);
      setLoader(false);
      setdisplayLang((prevState) => {
        if (prevState == 0) {
          return 1;
        } else {
          return 0;
        }
      });
    });
  };

  // console.log(props)
  const { isLoggedIn } = useSelector((state: RootState) => state.storage);

  const [BookmarkVisible, SetVisibility] = React.useState(0);
  // if bookmark alert not visible, 0 ; if successfully bookmarked , then 1 ; if not logged in then 2.

  // obj.description = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged"
  let [bookmark_url, set_bookmark_url] = React.useState(
    '/listing_pg/bookmark.png'
  );
  const queryid = useSelector((state: RootState) => state.storage.userID);

  let AlertComponent;

  if (BookmarkVisible == 0) {
    console.log('in state 0');
    <div></div>;
  } else if (BookmarkVisible == 1) {
    console.log('in state 1');
    AlertComponent = <Alert message="Bookmarked" type="warning" />;
  } else {
    console.log('in state 2');
    AlertComponent = <Alert message="Login First" type="error" />;
  }
  async function bookmark_handler() {
    const { apiUrl } = config;
    if (!isLoggedIn) {
      // alertService.error('Please Login First!!', {autoClose : true})
      // return
      SetVisibility(2);
    } else {
      const request_obj = {
        cus_uid: queryid.toString(),
        p_uid: props.obj.id.toString(),
      };
      const response = await fetch(
        `${apiUrl}/api/customers/${queryid}/bookmarks`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(request_obj),
        }
      );

      if (response.ok) {
        // alertService.success('Bookmarked', {autoClose : true})
        SetVisibility(1);
        set_bookmark_url('/listing_pg/yellow_bookmark.png');
      } else console.log(response);
    }
  }
  return (
    <div>
      <div className={st.alert}>{AlertComponent}</div>

      <div className={st.card_container}>
        <img src={obj.product_img_url} className={st.card_img1} />

        <div className={st.details1}>
          <img src={obj.company_img_url} className={st.card_img2} />
          <div className={st.contractor_div}>
            <div className={st.contractor}>{obj.contractor_name}</div>

            <img
              className={st.bookmarkimg}
              src={bookmark_url}
              onClick={bookmark_handler}
            />
          </div>
          <button className={st.btn} onClick={translateText}>
            {loader ? <Spinner /> : <div className={st.btntext}>Translate</div>}
          </button>
          <button className={st.btn} onClick={props.clicker}>
            <div className={st.btntext}>Connect</div>
          </button>
        </div>
        <div className={st.details2}>{translationText}</div>
      </div>
    </div>
  );
}
