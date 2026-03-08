# 프론트엔드 (Frontend)

- [소개](#introduction)
- [PHP 사용하기](#using-php)
    - [PHP와 Blade](#php-and-blade)
    - [Livewire](#livewire)
    - [스타터 키트](#php-starter-kits)
- [React, Svelte, 또는 Vue 사용하기](#using-react-svelte-or-vue)
    - [Inertia](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [에셋 번들링](#bundling-assets)

<a name="introduction"></a>
## 소개 (Introduction)

Laravel은 [라우팅](/docs/12.x/routing), [유효성 검증](/docs/12.x/validation), [캐싱](/docs/12.x/cache), [큐](/docs/12.x/queues), [파일 저장소](/docs/12.x/filesystem) 등, 현대적인 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 갖춘 백엔드 프레임워크입니다. 그러나 Laravel은 개발자에게 강력한 프론트엔드 개발 방식과 아름다운 풀스택 경험까지 제공하는 것이 중요하다고 생각합니다.

Laravel로 애플리케이션을 만들 때 프론트엔드 개발을 하는 주요 방법은 두 가지이며, 어떤 방식을 선택할지는 PHP를 활용할지, 아니면 React, Svelte, Vue와 같은 JavaScript 프레임워크를 사용할지에 따라 달라집니다. 아래에서 이 두 가지 접근 방식을 모두 살펴보고, 여러분의 애플리케이션에 가장 잘 맞는 프론트엔드 개발 방식을 선택할 수 있도록 안내하겠습니다.

<a name="using-php"></a>
## PHP 사용하기 (Using PHP)

<a name="php-and-blade"></a>
### PHP와 Blade (PHP and Blade)

과거에는 대부분의 PHP 애플리케이션이 데이터베이스에서 데이터를 받아와서, PHP `echo`문이 삽입된 간단한 HTML 템플릿을 렌더링하여 브라우저에 HTML을 출력했습니다:

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>
```

Laravel에서는 [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)를 사용해 이와 같은 HTML 렌더링 방식을 여전히 구현할 수 있습니다. Blade는 데이터 표시와 반복 등 다양한 작업을 간단하고 짧은 문법으로 처리할 수 있게 해주는 매우 경량의 템플릿 언어입니다:

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>
```

이 방식으로 애플리케이션을 개발할 때, 폼 전송이나 페이지 내 상호작용이 발생하면 서버에서 완전히 새로운 HTML 문서를 받아오며, 브라우저는 전체 페이지를 새로 렌더링합니다. 지금도 많은 애플리케이션에서는 이처럼 단순한 Blade 템플릿만으로도 충분히 프론트엔드를 구성할 수 있습니다.

<a name="growing-expectations"></a>
#### 높아진 사용자 기대치

하지만 웹 애플리케이션에 대한 사용자 기대치가 발전함에 따라, 더 세련되고 동적인 프론트엔드를 만들고자 하는 요구가 커졌습니다. 그래서 일부 개발자들은 React, Svelte, Vue 같은 자바스크립트 프레임워크를 이용해 프론트엔드 개발을 시작하기도 합니다.

반면 익숙한 백엔드 언어(PHP)에 머무르길 원하는 개발자들은, 주요 개발 언어(백엔드 언어)만으로도 현대적인 웹 애플리케이션 UI를 제작할 수 있는 솔루션을 만들어 왔습니다. 예를 들어 [Rails](https://rubyonrails.org/) 생태계에서는 [Turbo](https://turbo.hotwired.dev/), [Hotwire](https://hotwired.dev/), [Stimulus](https://stimulus.hotwired.dev/) 같은 라이브러리가 그렇습니다.

Laravel 생태계에서는 주로 PHP로 동적이고 현대적인 프론트엔드를 만들 필요성 때문에 [Laravel Livewire](https://livewire.laravel.com)와 [Alpine.js](https://alpinejs.dev/)가 만들어졌습니다.

<a name="livewire"></a>
### Livewire

[Laravel Livewire](https://livewire.laravel.com)는 Laravel을 기반으로 하면서 React, Svelte, Vue와 같은 최신 JavaScript 프레임워크로 만든 프론트엔드처럼 동적이고 현대적인 UI를 구현할 수 있게 해주는 프레임워크입니다.

Livewire를 사용할 때, 여러분은 프론트엔드의 한 부분을 렌더링하고, 메서드와 데이터를 외부에서 사용할 수 있게 하는 "Livewire 컴포넌트"를 만듭니다. 예를 들어, 간단한 "카운터(Counter)" 컴포넌트는 다음과 같이 작성될 수 있습니다:

```php
<?php

use Livewire\Component;

new class extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }
};
?>

<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>

```

보시는 것처럼, Livewire는 `wire:click`과 같은 HTML 속성을 사용할 수 있게 해서, Laravel 애플리케이션의 프론트엔드와 백엔드를 쉽게 연결해줍니다. 또한, 컴포넌트의 현재 상태를 간단한 Blade 표현식으로 렌더링할 수도 있습니다.

많은 개발자에게 Livewire는 Laravel에서의 프론트엔드 개발의 패러다임을 바꿔 주었으며, Laravel 환경에 익숙한 채로도 모던하고 동적인 웹 애플리케이션을 만들 수 있도록 해주었습니다. 보통 Livewire로 개발하는 분들은 [Alpine.js](https://alpinejs.dev/)를 함께 사용해서, 예를 들어 다이얼로그 창 렌더링처럼 필요한 곳에만 최소한의 자바스크립트를 추가하곤 합니다.

Laravel에 처음 입문하셨다면, 먼저 [뷰](/docs/12.x/views)와 [Blade](/docs/12.x/blade)의 기본 사용법을 익히신 후, 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참고해 Livewire 컴포넌트로 상호작용이 가능한 애플리케이션을 만들어 보시길 추천합니다.

<a name="php-starter-kits"></a>
### 스타터 키트 (Starter Kits)

PHP와 Livewire로 프론트엔드를 구축하고 싶다면, [Livewire 스타터 키트](/docs/12.x/starter-kits)를 이용해 애플리케이션 개발을 더욱 빠르게 시작할 수 있습니다.

<a name="using-react-svelte-or-vue"></a>
## React, Svelte, 또는 Vue 사용하기 (Using React, Svelte, or Vue)

Laravel과 Livewire만으로도 충분히 현대적인 프론트엔드를 만들 수 있으나, 더 많은 개발자들은 여전히 React, Svelte, Vue와 같은 JavaScript 프레임워크가 가진 강력함을 활용하기를 선호합니다. 이런 선택을 통해 개발자는 NPM을 통해 제공되는 다양한 JavaScript 패키지와 툴의 풍부한 생태계를 사용할 수 있습니다.

하지만 추가적인 도구 없이 Laravel을 React, Svelte, Vue와 연동하면, 클라이언트 사이드 라우팅, 데이터 하이드레이션, 인증(authentication)과 같은 복잡한 문제들을 직접 해결해야 합니다. 클라이언트 사이드 라우팅의 경우에는 [Next](https://nextjs.org/), [Nuxt](https://nuxt.com/) 같은 프레임워크가 해결해 주지만, 데이터 하이드레이션과 인증 문제는 여전히 복잡하고 번거롭게 남습니다.

또한, 백엔드와 프론트엔드 각각 별도의 코드 저장소를 관리해야 하고, 그에 따른 유지보수나 배포도 별도로 해야 하는 문제가 발생합니다. 이런 문제들은 극복이 불가능한 것은 아니지만, 개발에 있어 생산적이거나 즐거운 방식은 아닙니다.

<a name="inertia"></a>
### Inertia

다행히도, Laravel은 양쪽의 장점을 모두 누릴 수 있도록 해줍니다. [Inertia](https://inertiajs.com)는 Laravel 애플리케이션과 최신 React, Svelte, Vue 프론트엔드 사이를 연결해 주는 다리 역할을 합니다. 이를 통해 라우팅, 데이터 하이드레이션, 인증 등은 Laravel의 라우트와 컨트롤러를 그대로 사용하면서, React, Svelte, Vue로 적극적으로 프론트엔드를 개발할 수 있습니다. 모두 하나의 코드 저장소 내에서 이뤄지며, 두 환경의 장점을 모두 온전히 누릴 수 있습니다.

Inertia를 설치한 후, 기존과 동일하게 라우트와 컨트롤러를 작성하면 됩니다. 단, 컨트롤러에서는 Blade 템플릿을 반환하는 대신 Inertia 페이지를 반환하게 됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): Response
    {
        return Inertia::render('users/show', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```

여기서 Inertia 페이지는 React, Svelte, Vue 컴포넌트에 해당하는 것으로, 주로 애플리케이션의 `resources/js/pages` 디렉토리에 저장됩니다. 컨트롤러에서 `Inertia::render`로 넘긴 데이터는 페이지 컴포넌트의 "props"를 채우는 데 사용됩니다:

```jsx
import Layout from '@/layouts/authenticated';
import { Head } from '@inertiajs/react';

export default function Show({ user }) {
    return (
        <Layout>
            <Head title="Welcome" />
            <h1>Welcome</h1>
            <p>Hello {user.name}, welcome to Inertia.</p>
        </Layout>
    )
}
```

보시다시피 Inertia를 쓰면, 프론트엔드 개발에 있어 React, Svelte, Vue의 모든 기능을 온전히 활용할 수 있으면서도, Laravel 기반 백엔드와 JavaScript 기반 프론트엔드 사이를 가볍게 연결해주는 역할을 하게 됩니다.

#### 서버 사이드 렌더링

애플리케이션에 서버 사이드 렌더링(Server-Side Rendering)이 필요해서 Inertia 도입이 우려된다면 걱정하지 않으셔도 됩니다. Inertia는 [서버 사이드 렌더링 지원](https://inertiajs.com/server-side-rendering)을 제공합니다. 또한, [Laravel Cloud](https://cloud.laravel.com)나 [Laravel Forge](https://forge.laravel.com)에서 앱을 배포하면 Inertia의 서버 사이드 렌더링 프로세스를 손쉽게 항상 실행되도록 설정할 수 있습니다.

<a name="inertia-starter-kits"></a>
### 스타터 키트 (Starter Kits)

Inertia와 React / Svelte / Vue를 활용해 프론트엔드를 만들고 싶으신가요? [React, Svelte, Vue 애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 활용해 프로젝트의 개발을 바로 시작해 보세요. 이 스타터 키트들은 Inertia, React / Svelte / Vue, [Tailwind](https://tailwindcss.com), [Vite](https://vitejs.dev)를 이용한 프론트엔드 및 백엔드 인증 플로우 기본 구조를 미리 제공하므로, 여러분의 다음 아이디어 개발에 바로 집중할 수 있습니다.

<a name="bundling-assets"></a>
## 에셋 번들링 (Bundling Assets)

Blade와 Livewire로 프론트엔드를 개발하든, React / Svelte / Vue와 Inertia로 만들든, 프로덕션 용으로 CSS를 번들링할 필요가 있습니다. 물론, React, Svelte, Vue로 프론트엔드를 만든다면 컴포넌트도 브라우저에서 실행할 수 있는 JavaScript 에셋으로 번들링해야 합니다.

Laravel은 기본적으로 [Vite](https://vitejs.dev)를 사용해 에셋을 번들링합니다. Vite는 로컬 개발 시 매우 빠른 빌드 속도와 거의 즉각적인 HMR(Hot Module Replacement, 모듈 실시간 교체)을 제공합니다. 신규 Laravel 애플리케이션(모든 [스타터 키트](/docs/12.x/starter-kits) 포함)에는 `vite.config.js` 파일이 들어 있으며, Laravel용 경량 Vite 플러그인이 자동으로 로드되어 Vite를 매우 쉽게 사용할 수 있게 도와줍니다.

가장 빠르게 Laravel과 Vite를 시작하는 방법은 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 이용해 개발을 시작하는 것입니다. 이 스타터 키트는 프론트엔드와 백엔드 인증 구조까지 미리 갖춘 채로 프로젝트를 빠르게 출발할 수 있도록 해줍니다.

> [!NOTE]
> Vite를 Laravel과 함께 활용하는 방법에 대한 더 자세한 설명은 [에셋 번들링 및 컴파일에 관한 전용 문서](/docs/12.x/vite)를 확인하시기 바랍니다.
