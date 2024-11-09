import axios from "axios";
import {AuthUrl, RestUrls} from "./Urls";


export class RestDataSource {

  GetData = async (dataType, params=null, slug=null) =>
      this.SendRequest("get", RestUrls[dataType]+(slug ? slug+"/" : ""), (params || {}));

  StoreData = (dataType, data, params = null, slug = null) =>
      this.SendRequest("post", RestUrls[dataType]+(slug ? slug+"/" : "" ), (params || {}), data);

  UpdateData = (dataType, data, params = null, slug = null) =>
      this.SendRequest("put", RestUrls[dataType]+(slug ? slug+"/" : "" ), (params || {}), data);

    SendRequest(method, url, params, data) {
        const axiosInstance = axios.create({
            baseURL: AuthUrl,
            timeout: 5000,
            headers: {
                'Authorization': localStorage.getItem('webToken') ? "JWT " + localStorage.getItem('webToken') : null,
                'Content-Type': 'application/json',
                'accept': 'application/json',
            }
        });

        axiosInstance.interceptors.response.use(
            response => response,
            error => {
                const originalRequest = error.config;

                // Prevent infinite loops
                if (error.response.status === 401 && originalRequest.url === AuthUrl+'refresh/') {
                    localStorage.setItem("nextPage", window.location);
                    return Promise.reject(error);
                }

                if (error.response.data.code === "token_not_valid" &&
                    error.response.status === 401 &&
                    error.response.statusText === "Unauthorized")
                    {
                        const refreshToken = localStorage.getItem('refreshToken');

                        if (refreshToken){
                            const tokenParts = JSON.parse(atob(refreshToken.split('.')[1]));

                            // exp date in token is expressed in seconds, while now() returns milliseconds:
                            const now = Math.ceil(Date.now() / 1000);
                            //console.log(tokenParts.exp);

                            if (tokenParts.exp > now) {
                                return axiosInstance
                                .post('refresh/', {refresh: refreshToken})
                                .then((response) => {

                                    localStorage.setItem('webToken', response.data.access);
                                    localStorage.setItem('refreshToken', response.data.refresh);

                                    axiosInstance.defaults.headers['Authorization'] = "JWT " + response.data.access;
                                    originalRequest.headers['Authorization'] = "JWT " + response.data.access;

                                    return axiosInstance(originalRequest);
                                })
                                .catch(err => {
                                    //console.log(err)
                                });
                            }else{
                                //console.log("Refresh token is expired", tokenParts.exp, now);
                                localStorage.setItem("nextPage", window.location);
                                //window.location.href = '/login/';
                            }
                        }else{
                            //console.log("Refresh token not available.");
                            localStorage.setItem("nextPage", window.location);
                            //window.location.href = '/login/';
                        }
                }


              // specific error handling done elsewhere
              return Promise.reject(error);
          }
        );
        return axiosInstance.request({
              method, url, params, data
          });
    }

}