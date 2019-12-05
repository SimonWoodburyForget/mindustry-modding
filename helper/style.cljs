(ns style.core
  (:require
   [reagent.core :as r]
   ))

(.log js/console "[init] style.core")

;; ;; Immutable initial state of the page.
;; (def page (.. js/document -documentElement -outerHTML))
;; ;; (def page (.serializeToString (new js/XMLSerializer) js/document))
;; (.log js/console page)
;; (.log js/console (clj->js (hk/as-hiccup (hk/parse page))))

;; (def toc (-> js/document -document getElementById "table-of-contents"))
;; (def toc (.getElementById js/document "table-of-contents"))



;; (def node (.createElement js/document "APP"))
;; (def textnode (.createTextNode js/document "This is a button."))
;; (.appendChild node textnode)

;; (.prepend toc node)

(defonce toc (.getElementById js/document "table-of-contents"))
(defonce pa (.getElementById js/document "postamble"))
(defonce content (.getElementById js/document "content"))
(defonce body (.getElementById js/document "content"))

(defonce app (.appendChild (.-body js/document)
                            (.createElement js/document "APP")))
                            ;; ;; (get (.getElementsByClassName toc "text-table-of-contents") 0)
                            ;; (.-firstChild toc)))

(def menu-state (r/atom "false"))
(defn menu-toggle [state]
  (defn unshow []
    (.add (.-classList toc) "unshow")
    (.add (.-classList pa) "unshow")
    (.add (.-classList content) "unshow"))

  (defn show []
    (.remove (.-classList toc) "unshow")
    (.remove (.-classList pa) "unshow")
    (.remove (.-classList content) "unshow"))
  
  (if (= state "true")
    (show)
    (unshow))

  (.log js/console state)
  
  ;; (set! (.-(.-style js/console body)))
  
  (if (= state "true")
    "false" "true"))

(defn button-component []
  [:button#toggle {:class (if (= @menu-state "true")
                            "unshow" "show")
                   :on-click #(swap! menu-state menu-toggle)} "☰"])

(defn ^:export run []
  (r/render [button-component]
            app))

(run)

;; (defn ^:export run []
;;   (r/render [simple-example]
;;             (js/document.getElementById "app")))
