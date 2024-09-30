import {useAuthStore} from "~/store/auth";
import jwtDecode from "jwt-decode";

export default defineNuxtRouteMiddleware((to) => {
    const { isAuthenticated } = storeToRefs(useAuthStore());
    const token = useCookie('token');

    if (token.value) {
        isAuthenticated.value = true;
        try {
            const decodedToken = jwtDecode(token.value);
            console.log(decodedToken)
            const currentTime = Math.floor(Date.now() / 1000);

            if (decodedToken.exp && decodedToken.exp < currentTime) {
                isAuthenticated.value = false;
                token.value = null;
                return navigateTo('/login');
            } else {
                isAuthenticated.value = true;
            }
        } catch (error) {
            isAuthenticated.value = false;
            token.value = null;
            return navigateTo('/login');
        }
    }

    if (token.value && to?.name === 'login') {
        return navigateTo('/');
    }


    if (!token.value && to?.name !== 'login') {
        abortNavigation();
        return navigateTo('/login');
    }
});