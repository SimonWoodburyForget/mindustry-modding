;; Disclaimer: have no clue what I'm doing.
(ns style.core
  (:require
   [reagent.core :as r]
   [garden.core :refer [css]]
   [garden.selectors :refer [descendant]]
   ))

(defn by-id [id]
  (.getElementById js/document id))

(defn create-el [el]
  (.createElement js/document el))

(.log js/console "[init] style.core")

(defn set-style [style]
  (def el (create-el "style"))
  (set! (.-innerHTML el) style)
  (.setAttribute el "id" "dark-theme")
  (.appendChild (.-head js/document) el))

(defn remove-style [style]
  (def el (by-id style))
  (if el
    (.removeChild (.-parentNode el) el)))

(def dark-theme
  "body,
#table-of-contents code
{
    background:#202020;
    color:#edf0f2;
}


#content
{
    background: #202020;
    scrollbar-color: #a0a0a0 #595959;
}

code, pre, pre.src,
table,
td, td.org-left, td.org-right,
th, th.org-right, th.org-left,
div#table-of-contents
{
    background: #202020;
}

pre
{
    box-shadow: 3px 3px #eee;
}

a
{
    color: #ffa;
}

:target
{
    color: #202020;
    background: #ffa;
}

:target > code
{
    color: #ffa;
}


div.outline-2
{
    border-top: 2px solid #f0f0f0;
}

div.outline-3
{
    border-top: 2px solid #909090;
}

div.outline-4
{
    border-top: 2px solid #303030;
}

div.outline-5
{
    border-top: 2px solid #303030;
}

button.theme-toggle
{
    color: #202020;
}")

(def menu-state (r/atom false))
(defn menu-toggle [state]
  (defonce toc (by-id "table-of-contents"))
  (defonce pa (by-id "postamble"))
  (defonce content (by-id "content"))

  (defn unshow []
    (.add (.-classList toc) "unshow")
    (.add (.-classList pa) "unshow")
    (.add (.-classList content) "unshow"))
  (defn show []
    (.remove (.-classList toc) "unshow")
    (.remove (.-classList pa) "unshow")
    (.remove (.-classList content) "unshow"))
  (if state (show) (unshow))
  (if state false true))


(def home "https://simonwoodburyforget.github.io/mindustry-modding/")
(defn go-home []
  (set! (.-location js/window) home))

(defn last-theme []
  (.getItem js/localStorage "theme"))

(def saved-theme (= (.getItem js/localStorage "theme") "dark"))
(def dark-atom (r/atom (not saved-theme)))

(defn toggle-dark [state]
  (if state
    (do (.setItem js/localStorage "theme" "dark")
        (set-style dark-theme)
        fales)
    (do (.setItem js/localStorage "theme" nil)
        (remove-style "dark-theme")
        true)))

(defn button-component []
  [:div#toggle {:class (if @menu-state "unshow" "show")}
   [:button {:on-click #(swap! menu-state menu-toggle)} "☰"]
   [:button.theme-toggle {:on-click #(swap! dark-atom toggle-dark) } "c"]
   ])

(if saved-theme
  (do (set-style dark-theme)
      (reset! dark-atom false)))

(defn ^export run []
  (defonce app (.appendChild (.-body js/document)
                             (.createElement js/document "APP")))
  (r/render [button-component] app))

(set! (.-onload js/window) run)
