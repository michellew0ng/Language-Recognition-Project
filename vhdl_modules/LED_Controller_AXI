library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity LED_Controller_AXI is
    Port (
        -- AXI Signals
        S_AXI_ACLK      : in std_logic;
        S_AXI_ARESETN   : in std_logic;
        S_AXI_AWADDR    : in std_logic_vector(3 downto 0);
        S_AXI_AWVALID   : in std_logic;
        S_AXI_WDATA     : in std_logic_vector(31 downto 0);
        S_AXI_WVALID    : in std_logic;
        S_AXI_BREADY    : in std_logic;
        S_AXI_ARADDR    : in std_logic_vector(3 downto 0);
        S_AXI_ARVALID   : in std_logic;
        S_AXI_RREADY    : in std_logic;
        S_AXI_BVALID    : out std_logic;
        S_AXI_RVALID    : out std_logic;
        S_AXI_RDATA     : out std_logic_vector(31 downto 0);
        S_AXI_WREADY    : out std_logic;
        S_AXI_AWREADY   : out std_logic;
        S_AXI_ARREADY   : out std_logic;

        -- LED Control Signals
        clk             : in std_logic;
        reset           : in std_logic;
        led_out         : out std_logic  -- LED output signal
    );
end LED_Controller_AXI;

architecture Behavioral of LED_Controller_AXI is
    -- Internal signals
    signal command_reg     : std_logic_vector(7 downto 0) := (others => '0');
    signal command_valid   : std_logic := '0';
    signal duty_cycle      : std_logic_vector(7 downto 0) := (others => '0');
    signal pwm_counter     : std_logic_vector(7 downto 0) := (others => '0');
    signal led_state       : std_logic := '0';

begin

    -- AXI Write Process: Receive command from C code via AXI interface
    process(S_AXI_ACLK)
    begin
        if rising_edge(S_AXI_ACLK) then
            if S_AXI_ARESETN = '0' then
                command_reg <= (others => '0');
                command_valid <= '0';
                S_AXI_AWREADY <= '0';
                S_AXI_WREADY <= '0';
                S_AXI_BVALID <= '0';
            elsif S_AXI_AWVALID = '1' and S_AXI_WVALID = '1' then
                S_AXI_AWREADY <= '1';
                S_AXI_WREADY <= '1';
                command_reg <= S_AXI_WDATA(7 downto 0);  -- Capture the command
                command_valid <= '1';
                S_AXI_BVALID <= '1';
            else
                command_valid <= '0';
                S_AXI_AWREADY <= '0';
                S_AXI_WREADY <= '0';
                S_AXI_BVALID <= '0';
            end if;
        end if;
    end process;

    -- Command interpretation and setting duty cycle
    process(clk, reset)
    begin
        if reset = '1' then
            duty_cycle <= (others => '0');
            led_state <= '0';
        elsif rising_edge(clk) then
            if command_valid = '1' then
                case command_reg is
                    when "00000000" =>  -- Turn LED OFF
                        duty_cycle <= (others => '0');
                        led_state <= '0';
                    when "00000001" =>  -- Turn LED ON at full brightness
                        duty_cycle <= X"FF"; -- 100% duty cycle
                        led_state <= '1';
                    when others =>  -- Set brightness using PWM
                        duty_cycle <= command_reg;  -- Use received value as duty cycle (1-255)
                        led_state <= '1';
                end case;
            end if;
        end if;
    end process;

    -- PWM process to control LED brightness
    process(clk)
    begin
        if rising_edge(clk) then
            pwm_counter <= pwm_counter + 1;
            if led_state = '1' then
                if pwm_counter < duty_cycle then
                    led_out <= '1';  -- LED ON
                else
                    led_out <= '0';  -- LED OFF
                end if;
            else
                led_out <= '0';  -- LED OFF
            end if;
        end if;
    end process;

end Behavioral;
