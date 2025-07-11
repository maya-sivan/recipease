from agent_flow.agent_flow import MasterAgent


def main():
   master = MasterAgent()
   result = master.run_new_query(user_email="mayasivannj@gmail.com", query="I'm vegetarian and I'd like to eat some steak or burger.")
#    result = master.run_scheduled_query("687045ecddd80b94204d6ff1")

   print("Finished running. Final state: ", result)




if __name__ == "__main__":
   main()
