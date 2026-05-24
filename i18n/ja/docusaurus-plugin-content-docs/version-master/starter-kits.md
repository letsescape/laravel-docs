# スターターキット (Starter Kits)

- [Introduction](#introduction)
- [スターター キットを使用したアプリケーションの作成](#creating-an-application)
- [利用可能なスターター キット](#available-starter-kits)
    - [React](#react)
    - [Svelte](#svelte)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [スターターキットのカスタマイズ](#starter-kit-customization)
    - [React](#react-customization)
    - [Svelte](#svelte-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [Authentication](#authentication)
    - [機能の有効化と無効化](#enabling-and-disabling-features)
    - [ユーザー作成とパスワードのリセットのカスタマイズ](#customizing-actions)
    - [二要素認証](#two-factor-authentication)
    - [レート制限](#rate-limiting)
- [WorkOS AuthKit 認証](#workos)
- [イナーシャSSR](#inertia-ssr)
- [コミュニティが管理するスターター キット](#community-maintained-starter-kits)
- [よくある質問](#faqs)

<a name="introduction"></a>
## 導入 (Introduction)

新しい Laravel アプリケーションの構築をすぐに始められるように、[アプリケーションスターターキット](https://laravel.com/starter-kits) を提供させていただきます。これらのスターター キットを使用すると、次の Laravel アプリケーションの構築をスムーズに始めることができ、アプリケーションのユーザーを登録および認証するために必要なルート、コントローラ、ビューが含まれています。スターター キットは、[Laravel の強化](/docs/{{version}}/fortify) を使用して認証を提供します。

これらのスターター キットを使用しても構いませんが、必須ではありません。 Laravel の新しいコピーをインストールするだけで、独自のアプリケーションを最初から自由に構築できます。いずれにせよ、私たちはあなたが素晴らしいものを作り上げることを確信しています。

<a name="creating-an-application"></a>
## スターター キットを使用したアプリケーションの作成 (Creating an Application Using a Starter Kit)

スターターキットのいずれかを使用して新しい Laravel アプリケーションを作成するには、まず [PHPとLaravel CLIツールをインストールする](/docs/{{version}}/installation#installing-php) を実行する必要があります。すでに PHP と Composer がインストールされている場合は、Composer 経由で Laravel インストーラー CLI ツールをインストールできます。

```shell
composer global require laravel/installer
```

次に、Laravel インストーラー CLI を使用して、新しい Laravel アプリケーションを作成します。 Laravel インストーラーは、好みのスターター キットを選択するよう求めます。

```shell
laravel new my-app
```

Laravel アプリケーションを作成した後、NPM 経由でフロントエンドの依存関係をインストールし、Laravel 開発サーバーを起動するだけです。

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 開発サーバーを起動すると、Web ブラウザー ([http://localhost:8000](http://localhost:8000)) でアプリケーションにアクセスできるようになります。

<a name="available-starter-kits"></a>
## 利用可能なスターター キット (Available Starter Kits)

<a name="react"></a>
### 反応する

当社の React スターター キットは、[Inertia](https://inertiajs.com) を使用して React フロントエンドで Laravel アプリケーションを構築するための堅牢で最新の開始点を提供します。

Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの React アプリケーションを構築できます。これにより、React のフロントエンドのパワーと、Laravel の驚異的なバックエンドの生産性および超高速の Vite コンパイルを組み合わせて楽しむことができます。

React スターター キットは、React 19、TypeScript、Tailwind、および [shadcn/ui](https://ui.shadcn.com) コンポーネント ライブラリを利用します。

<a name="svelte"></a>
### スレンダー

当社の Svelte スターター キットは、[Inertia](https://inertiajs.com) を使用して Svelte フロントエンドを備えた Laravel アプリケーションを構築するための堅牢で最新の開始点を提供します。

Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの Svelte アプリケーションを構築できます。これにより、Svelte のフロントエンドのパワーと、Laravel の驚異的なバックエンドの生産性および超高速の Vite コンパイルを組み合わせて楽しむことができます。

Svelte スターター キットは、Svelte 5、TypeScript、Tailwind、および [shadcn-svelte](https://www.shadcn-svelte.com/) コンポーネント ライブラリを利用します。

<a name="vue"></a>
### ヴュー

Vue スターター キットは、[Inertia](https://inertiajs.com) を使用して Vue フロントエンドで Laravel アプリケーションを構築するための優れた開始点を提供します。

Inertia を使用すると、従来のサーバー側のルーティングとコントローラを使用して、最新の単一ページの Vue アプリケーションを構築できます。これにより、Vue のフロントエンドのパワーと、Laravel の驚異的なバックエンドの生産性および超高速の Vite コンパイルを組み合わせて楽しむことができます。

Vue スターター キットは、Vue Comboposition API、TypeScript、Tailwind、および [shadcn-vue](https://www.shadcn-vue.com/) コンポーネント ライブラリを利用します。

<a name="livewire"></a>
### Livewire

当社の Livewire スターター キットは、[Laravel Livewire](https://livewire.laravel.com) フロントエンドを使用して Laravel アプリケーションを構築するための完璧な開始点を提供します。

Livewire は、PHP だけを使用して動的でリアクティブなフロントエンド UI を構築する強力な方法です。これは、主に Blade テンプレートを使用し、React、Svelte、Vue などの JavaScript 駆動の SPA フレームワークのよりシンプルな代替手段を探しているチームに最適です。

Livewire スターター キットは、Livewire、Tailwind、および [フラックスUI](https://fluxui.dev) コンポーネント ライブラリを利用します。

<a name="starter-kit-customization"></a>
## スターターキットのカスタマイズ (Starter Kit Customization)

<a name="react-customization"></a>
### 反応する

当社の React スターター キットは、Inertia 2、React 19、Tailwind 4、および [shadcn/ui](https://ui.shadcn.com) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

フロントエンド コードの大部分は、`resources/js` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

追加の shadcn コンポーネントを公開するには、まず [公開したいコンポーネントを見つけます](https://ui.shadcn.com) を実行します。次に、`npx` を使用してコンポーネントを公開します。

```shell
npx shadcn@latest add switch
```

この例では、コマンドはスイッチ コンポーネントを `resources/js/components/ui/switch.tsx` に公開します。コンポーネントが公開されると、どのページでも使用できるようになります。

```jsx
import { Switch } from "@/components/ui/switch"

const MyPage = () => {
  return (
    <div>
      <Switch />
    </div>
  );
};

export default MyPage;
```

<a name="react-available-layouts"></a>
#### 利用可能なレイアウト

React スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/js/layouts/app-layout.tsx` ファイルの先頭にインポートされるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### サイドバーのバリエーション

サイドバーのレイアウトには、デフォルトのサイドバー バリアント、「インセット」バリアント、および「フローティング」バリアントの 3 つの異なるバリアントが含まれています。 `resources/js/components/app-sidebar.tsx` コンポーネントを変更することで、最も好みのバリアントを選択できます。

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### 認証ページのレイアウトのバリエーション

React スターター キットに含まれる認証ページ (ログイン ページや登録ページなど) にも、「シンプル」、「カード」、「分割」の 3 つの異なるレイアウト バリアントが提供されています。

認証レイアウトを変更するには、アプリケーションの `resources/js/layouts/auth-layout.tsx` ファイルの先頭にインポートされるレイアウトを変更します。

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
### スレンダー

当社の Svelte スターター キットは、Inertia 2、Svelte 5、Tailwind、および [shadcn-svelte](https://www.shadcn-svelte.com/) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

フロントエンド コードの大部分は、`resources/js` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

追加の shadcn-svelte コンポーネントを公開するには、まず [公開したいコンポーネントを見つけます](https://www.shadcn-svelte.com) を実行します。次に、`npx` を使用してコンポーネントを公開します。

```shell
npx shadcn-svelte@latest add switch
```

この例では、コマンドはスイッチ コンポーネントを `resources/js/components/ui/switch/switch.svelte` に公開します。コンポーネントが公開されると、どのページでも使用できるようになります。

```svelte
<script lang="ts">
    import { Switch } from '@/components/ui/switch'
</script>

<div>
    <Switch />
</div>
```

<a name="svelte-available-layouts"></a>
#### 利用可能なレイアウト

Svelte スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/js/layouts/AppLayout.svelte` ファイルの先頭にインポートされるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a name="svelte-sidebar-variants"></a>
#### サイドバーのバリエーション

サイドバーのレイアウトには、デフォルトのサイドバー バリアント、「インセット」バリアント、および「フローティング」バリアントの 3 つの異なるバリアントが含まれています。 `resources/js/components/AppSidebar.svelte` コンポーネントを変更することで、最も好みのバリアントを選択できます。

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="svelte-authentication-page-layout-variants"></a>
#### 認証ページのレイアウトのバリエーション

Svelte スターター キットに含まれる認証ページ (ログイン ページや登録ページなど) にも、「シンプル」、「カード」、「分割」の 3 つの異なるレイアウト バリアントが用意されています。

認証レイアウトを変更するには、アプリケーションの `resources/js/layouts/AuthLayout.svelte` ファイルの先頭にインポートされるレイアウトを変更します。

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
### ヴュー

Vue スターター キットは、Inertia 2、Vue 3 Comboposition API、Tailwind、および [shadcn-vue](https://www.shadcn-vue.com/) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

フロントエンド コードの大部分は、`resources/js` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

追加の shadcn-vue コンポーネントを公開するには、まず [公開したいコンポーネントを見つけます](https://www.shadcn-vue.com) を実行します。次に、`npx` を使用してコンポーネントを公開します。

```shell
npx shadcn-vue@latest add switch
```

この例では、コマンドはスイッチ コンポーネントを `resources/js/components/ui/Switch.vue` に公開します。コンポーネントが公開されると、どのページでも使用できるようになります。

```vue
<script setup lang="ts">
import { Switch } from '@/components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```

<a name="vue-available-layouts"></a>
#### 利用可能なレイアウト

Vue スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/js/layouts/AppLayout.vue` ファイルの先頭にインポートされるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### サイドバーのバリエーション

サイドバーのレイアウトには、デフォルトのサイドバー バリアント、「インセット」バリアント、および「フローティング」バリアントの 3 つの異なるバリアントが含まれています。 `resources/js/components/AppSidebar.vue` コンポーネントを変更することで、最も好みのバリアントを選択できます。

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### 認証ページのレイアウトのバリエーション

ログイン ページや登録ページなど、Vue スターター キットに含まれる認証ページにも、「シンプル」、「カード」、「分割」の 3 つの異なるレイアウト バリアントが提供されています。

認証レイアウトを変更するには、アプリケーションの `resources/js/layouts/AuthLayout.vue` ファイルの先頭にインポートされるレイアウトを変更します。

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

当社の Livewire スターター キットは、Livewire 4、Tailwind、および [フラックスUI](https://fluxui.dev/) で構築されています。すべてのスターター キットと同様に、バックエンドとフロントエンドのコードはすべてアプリケーション内に存在し、完全なカスタマイズが可能です。

フロントエンド コードの大部分は、`resources/views` ディレクトリにあります。コードを自由に変更して、アプリケーションの外観と動作をカスタマイズできます。

```text
resources/views
├── components            # Reusable components
├── flux                  # Customized Flux components
├── layouts               # Application layouts
├── pages                 # Livewire pages
├── partials              # Reusable Blade partials
├── dashboard.blade.php   # Authenticated user dashboard
├── welcome.blade.php     # Guest user welcome page
```

<a name="livewire-available-layouts"></a>
#### 利用可能なレイアウト

Livewire スターター キットには、「サイドバー」レイアウトと「ヘッダー」レイアウトという 2 つの異なる主なレイアウトから選択できます。サイドバー レイアウトがデフォルトですが、アプリケーションの `resources/views/layouts/app.blade.php` ファイルで使用されるレイアウトを変更することで、ヘッダー レイアウトに切り替えることができます。さらに、メインの Flux コンポーネントに `container` 属性を追加する必要があります。

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### 認証ページのレイアウトのバリエーション

Livewire スターター キットに含まれる認証ページ (ログイン ページや登録ページなど) にも、「シンプル」、「カード」、「分割」という 3 つの異なるレイアウト バリアントが用意されています。

認証レイアウトを変更するには、アプリケーションの `resources/views/layouts/auth.blade.php` ファイルで使用されるレイアウトを変更します。

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## 認証 (Authentication)

すべてのスターター キットは、[Laravel の強化](/docs/{{version}}/fortify) を使用して認証を処理します。 Fortify は、ログイン、登録、パスワードのリセット、電子メール検証などのためのルート、コントローラ、ロジックを提供します。

Fortify は、アプリケーションの `config/fortify.php` 構成ファイルで有効になっている機能に基づいて、次の認証ルートを自動的に登録します。

| ルート                              | 方法 | 説明                         |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`    | ログインフォームを表示する                  |
| `/login`                           | `POST`   | ユーザーを認証する                   |
| `/logout`                          | `POST`   | ユーザーをログアウトする                        |
| `/register`                        | `GET`    | 登録フォームを表示する           |
| `/register`                        | `POST`   | 新しいユーザーを作成する                     |
| `/forgot-password`                 | `GET`    | パスワードリセットリクエストフォームを表示する |
| `/forgot-password`                 | `POST`   | パスワードリセットリンクを送信する            |
| `/reset-password/{token}`          | `GET`    | パスワードリセットフォームを表示する         |
| `/reset-password`                  | `POST`   | パスワードを更新する                     |
| `/email/verify`                    | `GET`    | メール認証通知を表示する   |
| `/email/verify/{id}/{hash}`        | `GET`    | メールアドレスを確認してください                |
| `/email/verification-notification` | `POST`   | 確認メールを再送信する           |
| `/user/confirm-password`           | `GET`    | パスワード確認フォームを表示する  |
| `/user/confirm-password`           | `POST`   | パスワードを認証する                    |
| `/two-factor-challenge`            | `GET`    | 2FA チャレンジフォームを表示する          |
| `/two-factor-challenge`            | `POST`   | 2FA コードを検証する                     |

`php artisan route:list` Artisan コマンドを使用すると、アプリケーション内のすべてのルートを表示できます。

<a name="enabling-and-disabling-features"></a>
### 機能の有効化と無効化

どの Fortify 機能を有効にするかは、アプリケーションの `config/fortify.php` 構成ファイルで制御できます。

```php
use Laravel\Fortify\Features;

'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
    Features::twoFactorAuthentication([
        'confirm' => true,
        'confirmPassword' => true,
    ]),
],
```

機能を無効にするには、その機能エントリを `features` 配列からコメント アウトするか削除します。たとえば、パブリック登録を無効にするには、`Features::registration()` を削除します。

[React](#react)、[Svelte](#svelte)、または [Vue](#vue) スターター キットを使用する場合は、フロントエンド コード内の無効な機能のルートへの参照も削除する必要があります。たとえば、電子メール検証を無効にする場合は、React、Svelte、または Vue コンポーネント内の `verification` ルートへのインポートと参照を削除する必要があります。これらのスターター キットは、ビルド時にルート定義を生成するタイプ セーフ ルーティングに Wayfinder を使用するため、これが必要です。存在しないルートを参照すると、アプリケーションのビルドは失敗します。

<a name="customizing-actions"></a>
### ユーザー作成とパスワードのリセットのカスタマイズ

ユーザーがパスワードを登録またはリセットすると、Fortify はアプリケーションの `app/Actions/Fortify` ディレクトリにあるアクション クラスを呼び出します。

| ファイル                          | 説明                           |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | 新しいユーザーを検証して作成します       |
| `ResetUserPassword.php`       | ユーザーのパスワードを検証して更新します  |
| `PasswordValidationRules.php` | パスワード検証ルールを定義します     |

たとえば、アプリケーションの登録ロジックをカスタマイズするには、`CreateNewUser` アクションを編集する必要があります。

```php
public function create(array $input): User
{
    Validator::make($input, [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'max:255', 'unique:users'],
        'phone' => ['required', 'string', 'max:20'], // [tl! add]
        'password' => $this->passwordRules(),
    ])->validate();

    return User::create([
        'name' => $input['name'],
        'email' => $input['email'],
        'phone' => $input['phone'], // [tl! add]
        'password' => Hash::make($input['password']),
    ]);
}
```

<a name="two-factor-authentication"></a>
### 二要素認証

スターター キットには 2 要素認証 (2FA) が組み込まれており、ユーザーは TOTP 互換の認証アプリを使用してアカウントを保護できます。 2FA は、アプリケーションの `config/fortify.php` 構成ファイルの `Features::twoFactorAuthentication()` によってデフォルトで有効になります。

`confirm` オプションでは、2FA を完全に有効にする前にユーザーがコードを検証する必要がありますが、`confirmPassword` では、2FA を有効または無効にする前にパスワードの確認が必要です。詳細については、[Fortify の 2 要素認証ドキュメント](/docs/{{version}}/fortify#two-factor-authentication) を参照してください。

<a name="rate-limiting"></a>
### レート制限

レート制限により、ブルートフォース攻撃やログイン試行の繰り返しによって認証エンドポイントに負荷がかかるのを防ぎます。 Fortify のレート制限動作は、アプリケーションの `FortifyServiceProvider` でカスタマイズできます。

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="workos"></a>
## WorkOS AuthKit 認証 (WorkOS AuthKit Authentication)

デフォルトでは、React、Svelte、Vue、Livewire スターター キットはすべて、Laravel の組み込み認証システムを利用して、ログイン、登録、パスワードリセット、電子メール検証などを提供します。さらに、以下を提供する各スターター キットの [WorkOS認証キット](https://authkit.com) パワード バリアントも提供しています。

<div class="content-list" markdown="1">

- ソーシャル認証 (Google、Microsoft、GitHub、Apple)
- パスキー認証
- メールベースの「Magic Auth」
- SSO

</div>

WorkOS を認証プロバイダ [WorkOS アカウントが必要です](https://workos.com) として使用します。 WorkOS は、月間アクティブ ユーザー 100 万人までのアプリケーションに対して無料の認証を提供します。

WorkOS AuthKit をアプリケーションの認証プロバイダとして使用するには、`laravel new` 経由で新しいスターター キットを利用したアプリケーションを作成するときに、WorkOS オプションを選択します。

### WorkOS スターター キットの構成

WorkOS 搭載スターター キットを使用して新しいアプリケーションを作成した後、アプリケーションの `.env` ファイルに `WORKOS_CLIENT_ID`、`WORKOS_API_KEY`、および `WORKOS_REDIRECT_URL` 環境変数を設定する必要があります。これらの変数は、アプリケーションの WorkOS ダッシュボードで提供される値と一致する必要があります。

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

さらに、WorkOS ダッシュボードでアプリケーションのホームページ URL を構成する必要があります。この URL は、ユーザーがアプリケーションからログアウトした後にリダイレクトされる場所です。

<a name="configuring-authkit-authentication-methods"></a>
#### AuthKit 認証方法の構成

WorkOS を利用したスターター キットを使用する場合は、アプリケーションの WorkOS AuthKit 構成設定内で「電子メール + パスワード」認証を無効にし、ユーザーがソーシャル認証プロバイダ、パスキー、「Magic Auth」、および SSO を介してのみ認証できるようにすることをお勧めします。これにより、アプリケーションはユーザー パスワードの処理を完全に回避できます。

<a name="configuring-authkit-session-timeouts"></a>
#### AuthKit セッションのタイムアウトの構成

さらに、Laravel アプリケーションに設定されているセッション タイムアウトしきい値 (通常は 2 時間) と一致するように、WorkOS AuthKit セッションの非アクティブ タイムアウトを設定することをお勧めします。

<a name="inertia-ssr"></a>
### イナーシャSSR

React、Svelte、および Vue スターター キットは、Inertia の [サーバーサイドレンダリング](https://inertiajs.com/server-side-rendering) 機能と互換性があります。アプリケーション用の Inertia SSR 互換バンドルを構築するには、`build:ssr` コマンドを実行します。

```shell
npm run build:ssr
```

便宜上、`composer dev:ssr` コマンドも使用できます。このコマンドは、アプリケーション用の SSR 互換バンドルを構築した後、Laravel 開発サーバーと Inertia SSR サーバーを起動し、Inertia のサーバー側レンダリング エンジンを使用してアプリケーションをローカルでテストできるようにします。

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### コミュニティが管理するスターター キット

Laravel インストーラーを使用して新しい Laravel アプリケーションを作成する場合、Packagist で入手可能なコミュニティが管理するスターター キットを `--using` フラグに提供できます。

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### スターターキットの作成

スターター キットを他の人が確実に利用できるようにするには、[Packagist](https://packagist.org) に公開する必要があります。スターター キットは、`.env.example` ファイルで必要な環境変数を定義する必要があり、必要なインストール後のコマンドはスターター キットの `composer.json` ファイルの `post-create-project-cmd` 配列にリストされている必要があります。

<a name="faqs"></a>
### よくある質問

<a name="faq-upgrade"></a>
#### アップグレードするにはどうすればよいですか?

すべてのスターター キットは、次のアプリケーションへの確実な出発点となります。コードの完全な所有権があれば、思い描いたとおりにアプリケーションを調整、カスタマイズ、構築できます。ただし、スターター キット自体をアップデートする必要はありません。

<a name="faq-enable-email-verification"></a>
#### 電子メール認証を有効にするにはどうすればよいですか?

電子メール検証を追加するには、`App/Models/User.php` モデル内の `MustVerifyEmail` インポートのコメントを解除し、モデルが `MustVerifyEmail` インターフェイスを実装していることを確認します。

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
// ...

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```

登録後、ユーザーは確認メールを受け取ります。ユーザーの電子メール アドレスが確認されるまで特定のルートへのアクセスを制限するには、`verified` ミドルウェアをルートに追加します。

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> スターター キットの [WorkOS](#workos) バリアントを使用する場合、電子メール検証は必要ありません。

<a name="faq-modify-email-template"></a>
#### デフォルトの電子メール テンプレートを変更するにはどうすればよいですか?

デフォルトの電子メール テンプレートをカスタマイズして、アプリケーションのブランドに合わせることもできます。このテンプレートを変更するには、次のコマンドを使用して電子メール ビューをアプリケーションに公開する必要があります。

```
php artisan vendor:publish --tag=laravel-mail
```

これにより、`resources/views/vendor/mail` にいくつかのファイルが生成されます。これらのファイルと `resources/views/vendor/mail/themes/default.css` ファイルを変更して、デフォルトの電子メール テンプレートの外観を変更できます。

