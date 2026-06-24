<!-- # Laravel Mix -->
# Laravel Mix

- [Introduction](#introduction)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!WARNING]
> Laravel Mix は、現在は積極的にメンテナンスされていないレガシー パッケージです。 [Vite](/docs/13.x/vite) は最新の代替手段として使用できます。

<!-- [Laravel Mix](https://github.com/laravel-mix/laravel-mix), a package developed by [Laracasts](https://laracasts.com) creator Jeffrey Way, provides a fluent API for defining [webpack](https://webpack.js.org) build steps for your Laravel application using several common CSS and JavaScript pre-processors. -->
[Laravel Mix](https://github.com/laravel-mix/laravel-mix) は、[Laracasts](https://laracasts.com) の作成者である Jeffrey Way によって開発されたパッケージで、いくつかの一般的な CSS および JavaScript プリプロセッサを使用して、Laravel アプリケーションの [webpack](https://webpack.js.org) ビルドステップを定義するための流暢な API を提供します。

<!-- In other words, Mix makes it a cinch to compile and minify your application's CSS and JavaScript files. Through simple method chaining, you can fluently define your asset pipeline. For example: -->
言い換えれば、Mix を使用すると、アプリケーションの CSS ファイルと JavaScript ファイルのコンパイルと縮小が簡単になります。シンプルなメソッドチェーンを通じて、アセットパイプラインをスムーズに定義できます。例えば：

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

<!-- If you've ever been confused and overwhelmed about getting started with webpack and asset compilation, you will love Laravel Mix. However, you are not required to use it while developing your application; you are free to use any asset pipeline tool you wish, or even none at all. -->
Webpack とアセットのコンパイルを開始する際に混乱したり圧倒されたりしたことがあれば、Laravel Mix を気に入るはずです。ただし、アプリケーションの開発中にこれを使用する必要はありません。希望するアセット パイプライン ツールを自由に使用することも、まったく使用しないこともできます。

> [!NOTE]
> Vite は、新しい Laravel インストールで Laravel Mix を置き換えました。 Mix のドキュメントについては、[official Laravel Mix](https://laravel-mix.com/) Web サイトをご覧ください。 Vite に切り替えたい場合は、[Vite migration guide](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite) をご覧ください。

