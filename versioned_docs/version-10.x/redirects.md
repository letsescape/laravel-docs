<!-- # HTTP Redirects -->
# HTTP Redirects

- [Creating Redirects](#creating-redirects)
- [Redirecting To Named Routes](#redirecting-named-routes)
- [Redirecting To Controller Actions](#redirecting-controller-actions)
- [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
<!-- ## Creating Redirects -->
## Creating Redirects

<!-- Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper: -->
리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 이동시키는 데 필요한 올바른 헤더를 포함하고 있습니다. `RedirectResponse` 인스턴스를 생성하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다.

```
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

<!-- Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/10.x/session), make sure the route calling the `back` function is using the `web` middleware group or has all of the session middleware applied: -->
폼 제출이 잘못되어 사용자를 이전 위치로 되돌리고 싶을 때도 있습니다. 이럴 때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [session](/docs/10.x/session)을 활용하므로, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용하거나 모든 세션 미들웨어가 적용되어 있어야 합니다.

```
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
<!-- ## Redirecting To Named Routes -->
## Redirecting To Named Routes

<!-- When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method: -->
`redirect` 헬퍼를 파라미터 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어, `Redirector` 인스턴스의 다양한 메서드를 사용할 수 있습니다. 예를 들어, 네임드 라우트로 `RedirectResponse`를 만들고 싶다면 `route` 메서드를 사용하면 됩니다.

```
return redirect()->route('login');
```

<!-- If your route has parameters, you may pass them as the second argument to the `route` method: -->
라우트에 파라미터가 필요한 경우, 두 번째 인수로 `route` 메서드에 파라미터를 전달할 수 있습니다.

```
// For a route with the following URI: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<!-- For convenience, Laravel also offers the global `to_route` function: -->
좀 더 편리하게 사용할 수 있도록, Laravel에서는 전역 `to_route` 함수도 제공합니다.

```
return to_route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
<!-- #### Populating Parameters Via Eloquent Models -->
#### Populating Parameters Via Eloquent Models

<!-- If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically: -->
만약 "ID" 파라미터가 필요한 라우트로 리다이렉트할 때, Eloquent 모델에서 해당 값을 가져오고 싶다면 모델 자체를 바로 전달할 수 있습니다. 그러면 모델의 ID가 자동으로 추출되어 사용됩니다.

```
// For a route with the following URI: profile/{id}

return redirect()->route('profile', [$user]);
```

<!-- If you would like to customize the value that is placed in the route parameter, you should override the `getRouteKey` method on your Eloquent model: -->
라우트 파라미터로 전달되는 값을 직접 지정하고 싶을 때는, Eloquent 모델에서 `getRouteKey` 메서드를 오버라이드하면 됩니다.

```
/**
 * Get the value of the model's route key.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
<!-- ## Redirecting To Controller Actions -->
## Redirecting To Controller Actions

<!-- You may also generate redirects to [controller actions](/docs/10.x/controllers). To do so, pass the controller and action name to the `action` method: -->
[controller actions](/docs/10.x/controllers)으로 리다이렉트 응답을 생성할 수도 있습니다. 이를 위해, 컨트롤러와 액션명을 `action` 메서드에 전달하세요.

```
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

<!-- If your controller route requires parameters, you may pass them as the second argument to the `action` method: -->
만약 컨트롤러 라우트에 파라미터가 필요하다면, 두 번째 인수로 `action` 메서드에 파라미터를 넘겨주면 됩니다.

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
<!-- ## Redirecting With Flashed Session Data -->
## Redirecting With Flashed Session Data

<!-- Redirecting to a new URL and [flashing data to the session](/docs/10.x/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain: -->
새로운 URL로 리다이렉트하면서 동시에 [flashing data to the session](/docs/10.x/session#flash-data)하는 경우가 많습니다. 보통 어떤 작업에 성공했을 때, 성공 메시지를 세션에 플래시하고 리다이렉트하곤 합니다. Laravel에서는 이를 쉽게 할 수 있도록, 하나의 메서드 체인으로 `RedirectResponse` 인스턴스를 생성하고 데이터를 세션에 플래시할 수 있습니다.

```
Route::post('/user/profile', function () {
    // Update the user's profile...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

<!-- You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. Once the input has been flashed to the session, you may easily [retrieve it](/docs/10.x/requests#retrieving-old-input) during the next request: -->
`RedirectResponse` 인스턴스의 `withInput` 메서드를 사용하면, 현재 요청의 입력값을 세션에 플래시한 뒤 사용자를 새로운 위치로 리다이렉트할 수 있습니다. 이렇게 입력값이 세션에 플래시되면, 다음 요청 시 [retrieve it](/docs/10.x/requests#retrieving-old-input).

```
return back()->withInput();
```

<!-- After the user is redirected, you may display the flashed message from the [session](/docs/10.x/session). For example, using [Blade syntax](/docs/10.x/blade): -->
사용자가 리다이렉트된 이후에는, [session](/docs/10.x/session)에서 플래시된 메시지를 출력할 수 있습니다. 예를 들어, [Blade syntax](/docs/10.x/blade)을 사용하여 아래와 같이 표시할 수 있습니다.

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```
