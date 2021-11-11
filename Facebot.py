from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time

class Face_bot():

    def __init__(self, driver: webdriver, post_link: str) -> None:
        
        self.driver = driver
        self.post_link = post_link
    
    def login(self, user: str, pass_word: str) -> None:
        """Faz login na conta do Facebook"""
        username= self.driver.find_element_by_name("email")
        password= self.driver.find_element_by_name("pass")
        
        #limpa o formulário
        username.clear()
        password.clear()

        #preenche o formulário
        username.send_keys(user)
        password.send_keys(pass_word)
      
        #click em login
        self.driver.find_element_by_name("login").click()
        time.sleep(3)

        #Redireciona para a página do POST a ser extraído
        self.driver.get(self.post_link)

    def getComments(self) -> list:
        """Coleta os comentários"""
        comments = []

        #divs html que contêm os comentários e usuários
        container = self.driver.find_elements_by_class_name('_680y')
        for div in container:
            comments.append(div.find_element_by_css_selector('div[style="text-align: start;"]').text)

        return comments

    def getUsers(self) -> list:
        """Coleta os usuários"""
        users = []
        #divs html que contêm os comentários e usuários
        container = self.driver.find_elements_by_class_name('_680y')

        for div in container:
           users.append(div.find_element_by_class_name('pq6dq46d').text)

        return users

    def load_more_comment(self,count: int) -> tuple:
        """Abrir popup de opções de comentários escolhe a opção todos os comentários  aperta o botão mais comentários 
        Coleta os comentários e usuários adiciona cada um em uma lista e retorna as duas listas numa tupla"""
        
        comments =[]
        users = []
        #Abri o pop up de opções de comentários
        pop_up = self.driver.find_element_by_class_name('bp9cbjyn.j83agx80.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.h3fqq6jp').click()
        time.sleep(1)
        #Opções de comentários
        pop_up = self.driver.find_element_by_css_selector('div[style="transform: translate(0px, 0px);"]')
        options = pop_up.find_elements_by_css_selector('div[role="menuitem"]')
        #Opção: mais comentários
        options[2].click()
        time.sleep(2)
        
        #botão ver mais comentários
        button = self.driver.find_element_by_xpath("//span[contains(text(), 'Ver mais')]")
        self.driver.execute_script('arguments[0].scrollIntoView(true);', button)
        i = 0
        while i < count:
              try:
                  comments.extend(self.getComments())
                  users.extend(self.getUsers())
                  button.click()
                  time.sleep(3)
                  self.driver.execute_script('arguments[0].scrollIntoView(true);', button)
              except (NoSuchElementException, StaleElementReferenceException) as e:
                  print("Botão não está visível!")
                  pass

              i +=1
        return (users, comments)

    def close(self) -> None:
        """Faz logout e fecha o navegador"""
        
        #Abrir o pop up com opções da conta
        self.driver.find_element_by_css_selector('div[aria-label="Conta"]').click()
    
        time.sleep(2)
        #click em sair
        self.driver.find_element_by_class_name('qzhwtbm6.knvmm38d').click()

        time.sleep(1)
        #fecha o navegador
        self.driver.quit()