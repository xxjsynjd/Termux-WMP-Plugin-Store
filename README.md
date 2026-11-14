# Termux-WMP-Plugin-Store
The official plugin repository and web store for TWMPXPEM (Termux-Windows-Media-Player-XP-Extension-Manager).
# 🚀 TWMXPEM插件商店(Termux WMP Plugin Store)

欢迎来到 **TEMPXPEM** 生态的官方应用商店！
我们致力于在Termux上打造极致的“音频驱动视觉”渲染体验。

## 🏛️ 这是什么？
这是基于GitHub Pages和GitHub Actions搭建的全自动插件分发中心。
我们采用完全对齐Debian APT仓库的 `pool` 池化架构，并拥有自动打包加壳(TWMP专属格式)的流水线。

## 🎨 我是插件开发者，我该怎么提交我的特效？
只需3步，你的特效就能上架商店：
1. 在 `plugins/` 目录下新建一个文件夹(比如 `my_cyberpunk_glitch`)。
2. 在里面放入你的 `twmpxpem-project.toml` 和 `wmpvisualizer.dll`(纯Python代码)。
3. 提交Pull Request。
*机器人会自动帮你打包、加壳并生成索引，审核通过后瞬间全网上架！*

👉 **[点击这里查看《插件开发指南》(Coming Soon)]**

## 📦 我是普通用户，我怎么用？
在你的Termux中配置源并安装：
```bash
# 添加软件源
echo "wvwhl https://xxjsynjd.github.io/Termux-WMP-Plugin-Store termux-main main" >> $PREFIX/etc/twmpxpem/sources.list

# 安装你想用的特效
twmpxpem install edm_glowing_sphere
```

## 🛠️ 核心技术栈
*   **Package Manager**: 自研 `twmpxpem`(复刻dpkg/apt哲学)
*   **Rendering Engine**: `wmpvisualizer1`(FFmpeg+多声道FFT)
*   **Automation**: GitHub Actions自动打包与加壳
